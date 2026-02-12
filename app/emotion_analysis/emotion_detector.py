from transformers import pipeline

emotion_model = pipeline("sentiment-analysis",   model="j-hartmann/emotion-english-distilroberta-base")

emotion_pipe = pipeline(
    "audio-classification",
    model="superb/hubert-large-superb-er"
)

def detect_emotion(text):
    if text.strip() == "":
        return "Neutral"

    result = emotion_model(text)[0]
    return result["label"]



def detect_voice_emotion(audio_file):
    result_emotion = emotion_pipe(audio_file)
    return result_emotion[0]["label"]