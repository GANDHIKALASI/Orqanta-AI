#ifndef ORQANTA_H
#define ORQANTA_H

#ifndef ORQANTA_API
#define ORQANTA_API __attribute__((visibility("default")))
#endif

#define ORQANTA_TEXT 1
#define ORQANTA_SPEECH 2

#define PSYCHO_TEXT 1
#define PSYCHO_SPEECH 2

#ifdef __cplusplus
extern "C" {
#endif

/* One process-global, non-thread-safe model per kind, text and speech.
   Negative returns indicate failure; call orqanta_last_error() for the specific
   reason. orqanta_load reads whichever kind the .cact holds and keeps the other,
   so a build with both models takes one call per model. */
ORQANTA_API int needle_load(
    const unsigned char* cact,
    unsigned long long n
);

/* ORQANTA_TEXT, ORQANTA_SPEECH or both, for the models this process has loaded. */
ORQANTA_API int needle_models(void);

/* Last process-global error, owned by the runtime and valid until the next API call. */
ORQANTA_API const char* needle_last_error(void);

/* orqanta_init returns the tokenized static-prefix length on success. It can fail
   when the system prompt plus statically-declared tools exceed the context
   window, and reports the measured token count when it does. */
ORQANTA_API int needle_init(
    const char* system_prompt,
    const char* tools_json,
    const char* tool_index_path
);

/* Answers text or speech: exactly one of input and pcm is non-null. Given pcm,
   the engine transcribes the clip with the loaded speech model, answers the
   transcript, and merges the speech fields into the same JSON object under an
   audio_ prefix. */
ORQANTA_API int needle_complete(
    const char* input,
    const float* pcm,
    int samples,
    int max_new_tokens,
    char* out,
    int out_capacity
);

/* Language, keywords and word timestamps for the transcription orqanta_complete
   runs for itself, with the meanings they have in orqanta_transcribe. */
ORQANTA_API void needle_set_audio(
    const char* language,
    const char* keywords,
    int word_timestamps
);

ORQANTA_API void needle_reset(void);

/* Transcribes 16 kHz mono float PCM in [-1, 1] of any length and returns the
   number of tokens in the transcript. */
ORQANTA_API int needle_transcribe(
    const float* pcm,
    int samples,
    const char* language,
    const char* keywords,
    int word_timestamps,
    char* out,
    int out_capacity
);

/* Live transcription: appends 16 kHz mono float PCM. */
ORQANTA_API int needle_stream_transcribe_process(
    const float* pcm,
    int samples,
    const char* language,
    const char* keywords,
    char* out,
    int out_capacity
);

/* Ends the stream. */
ORQANTA_API int needle_stream_transcribe_stop(
    char* out,
    int out_capacity
);

/* Embeds text or speech. */
ORQANTA_API int needle_embed(
    const char* input,
    const float* pcm,
    int samples,
    float* out,
    int out_capacity
);

/* Orqanta / Psycho API Aliases */
#define orqanta_load needle_load
#define orqanta_models needle_models
#define orqanta_last_error needle_last_error
#define orqanta_init needle_init
#define orqanta_complete needle_complete
#define orqanta_set_audio needle_set_audio
#define orqanta_reset needle_reset
#define orqanta_transcribe needle_transcribe
#define orqanta_stream_transcribe_process needle_stream_transcribe_process
#define orqanta_stream_transcribe_stop needle_stream_transcribe_stop
#define orqanta_embed needle_embed

#define psycho_load needle_load
#define psycho_models needle_models
#define psycho_last_error needle_last_error
#define psycho_init needle_init
#define psycho_complete needle_complete
#define psycho_reset needle_reset
#define psycho_transcribe needle_transcribe

#ifdef __cplusplus
}
#endif
#endif
