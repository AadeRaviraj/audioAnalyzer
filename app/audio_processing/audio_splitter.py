# audio_processing/audio_splitter.py
import librosa
import io

def split_audio(audio_bytes, chunk_duration=3.0 ,sr=16000):

    if isinstance(audio_bytes,bytes):
        y, sr = librosa.load(io.BytesIO(audio_bytes), sr=sr)
    else:
        y, sr = librosa.load(audio_bytes, sr=sr) 

    samples_per_chunk = int(chunk_duration * sr)
    chunks_with_time = []

    for i in range(0, len(y), samples_per_chunk): # step the every chunk by 3 
        chunk = y[i:i + samples_per_chunk]
        # chunks_with_time.append(chunk)
        if len(chunk) < sr * 1.0: 
            continue
        
        start_time_sec = i / sr 
        minutes = int(start_time_sec // 60)
        seconds = int(start_time_sec % 60)
        time_str = f"{minutes:02d}:{seconds:02d}"

        chunks_with_time.append({
            "time": time_str,
            "audio_chunk": chunk
        })
    return chunks_with_time,sr
