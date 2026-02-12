import faster_whisper as fw
import numpy as np

model = fw.WhisperModel(
    "tiny.en",
    device="cpu",
    compute_type="int8",
    cpu_threads=1
)

def chunk_script(audio_chunk, sr=16000):

    if len(audio_chunk) < sr * 1.0:
        return ""

    audio = audio_chunk.astype(np.float32)

    if audio.ndim == 2:
        audio = np.mean(audio, axis=1)

    # Skip silent chunks
    if np.mean(np.abs(audio)) < 0.005:
        return ""

    print("Chunk size:", len(audio))

    segments, _ = model.transcribe(
        audio,
        language="en",
        beam_size=1,      # FAST
        vad_filter=True   # Remove silence automatically
    )

    text = " ".join(seg.text for seg in segments)

    if text.strip() == "":
        return "[silence]"

    return text.strip()
