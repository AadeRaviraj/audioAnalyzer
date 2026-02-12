import streamlit as st
import tempfile
import pandas as pd

from app.audio_processing.audio_splitter import split_audio
from app.speech_to_text.speech_converter import chunk_script
from app.emotion_analysis.emotion_detector import detect_emotion

st.set_page_config(page_title="Voice Emotion Analyzer")

st.title("Voice Emotion Analyzer")

uploaded_file = st.file_uploader("Upload Audio File", type=["wav", "mp3"])

if uploaded_file is not None:

    st.audio(uploaded_file)

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(uploaded_file.read())
        temp_path = tmp.name

    st.write("Processing...")

    chunks, sr = split_audio(temp_path)

    transcription = []
    emotion_log = []

    for chunk in chunks:
        text = chunk_script(chunk["audio_chunk"], sr)

        if text.strip() == "":
            continue

        transcription.append(text)

        emotion = detect_emotion(text)

        emotion_log.append({
            "time": chunk["time"],
            "emotion": emotion
        })

    st.subheader("Recognized Text")
    st.write(" ".join(transcription))

    if emotion_log:
        df = pd.DataFrame(emotion_log)
        st.subheader("Emotion Timeline")
        st.dataframe(df)
        st.line_chart(df.set_index("time")["emotion"])
