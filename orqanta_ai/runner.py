from __future__ import annotations

import json
import os
import platform
import subprocess
import tempfile
from typing import Any, Dict, List, Optional

def find_orqanta_binary() -> Optional[str]:
    """Locate the standalone Orqanta / Psycho binary for the current architecture."""
    env_bin = os.environ.get("ORQANTA_BIN") or os.environ.get("PSYCHO_BIN")
    if env_bin and os.path.exists(env_bin):
        return env_bin

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    machine = platform.machine().lower()

    if machine in ("x86_64", "amd64"):
        candidate = os.path.join(base_dir, "bin", "linux-x86_64", "orqanta")
        if os.path.exists(candidate):
            return candidate
    elif machine in ("aarch64", "arm64", "armv8l"):
        candidate = os.path.join(base_dir, "bin", "android-arm64", "orqanta")
        if os.path.exists(candidate):
            return candidate

    import shutil
    for cmd in ("orqanta", "orqanta-ai", "psycho", "needle"):
        found = shutil.which(cmd)
        if found:
            return found

    return None

def find_orqanta_model() -> Optional[str]:
    """Locate the default base weights (.cact) model file."""
    env_model = os.environ.get("ORQANTA_MODEL") or os.environ.get("PSYCHO_MODEL")
    if env_model and os.path.exists(env_model):
        return env_model

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    candidates = [
        os.path.join(base_dir, "models", "orqanta.cact"),
        os.path.join(base_dir, "models", "needle3.cact"),
        os.path.expanduser("~/.cache/orqanta-ai/models/orqanta.cact"),
    ]
    for c in candidates:
        if os.path.exists(c):
            return c

    # Automatic download fallback from Hugging Face Hub (buggandhi/Orqanta-AI)
    try:
        from huggingface_hub import hf_hub_download
        cached = hf_hub_download(
            repo_id="buggandhi/Orqanta-AI",
            filename="models/orqanta.cact",
        )
        if cached and os.path.exists(cached):
            return cached
    except Exception:
        pass

    return None

def run_native_completion(
    prompt: str,
    tools: Optional[List[Dict[str, Any]]] = None,
    system: Optional[str] = None,
    weights_path: Optional[str] = None,
    binary_path: Optional[str] = None,
    max_tokens: int = 512,
) -> Dict[str, Any]:
    """Run one-shot tool-calling completion using the standalone Orqanta engine."""
    bin_path = binary_path or find_orqanta_binary()
    if not bin_path:
        raise RuntimeError(
            "Could not locate the Orqanta binary for your architecture. "
            "Please compile or set the ORQANTA_BIN environment variable."
        )

    model_path = weights_path or find_orqanta_model()
    if not model_path:
        raise RuntimeError(
            "Could not locate Orqanta model weights (.cact). "
            "Please ensure models/orqanta.cact exists or set ORQANTA_MODEL."
        )

    cmd = [bin_path, "--model", model_path, "--max", str(max_tokens)]
    tmp_files = []

    try:
        if tools:
            tools_f = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False)
            json.dump(tools, tools_f)
            tools_f.flush()
            tools_f.close()
            tmp_files.append(tools_f.name)
            cmd.extend(["--tools", tools_f.name])

        if system:
            sys_f = tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False)
            sys_f.write(system)
            sys_f.flush()
            sys_f.close()
            tmp_files.append(sys_f.name)
            cmd.extend(["--system", sys_f.name])

        cmd.extend(["--prompt", prompt])

        proc = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=10,
        )

        if proc.returncode != 0:
            raise RuntimeError(f"Orqanta engine exited with code {proc.returncode}: {proc.stderr}")

        output = proc.stdout.strip()
        # Find the JSON response line in stdout
        for line in reversed(output.splitlines()):
            line = line.strip()
            if line.startswith("{") and line.endswith("}"):
                return json.loads(line)

        raise RuntimeError(f"Invalid output format from engine: {output}")

    finally:
        for p in tmp_files:
            try:
                os.unlink(p)
            except OSError:
                pass
