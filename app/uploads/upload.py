from flask import Flask,request,redirect,jsonify, Blueprint,send_file
import io  
from ..audio_processing.audio_splitter import split_audio
from ..speech_to_text import speech_converter as SC
from ..emotion_analysis.emotion_detector import detect_emotion,detect_voice_emotion
import mimetypes

# import librosa



# Create a Blueprint
upload_bp = Blueprint("upload_bp", __name__)
audio_storage = {}

@upload_bp.route("/upload", methods=["POST"])
def upload():  
    if "audio_file" not in request.files:
            return "No file in request file"
        
    file = request.files["audio_file"]
    if file == "":
        return "No such a file selected....."
    
    if not file.filename.lower().endswith(('.wav','.mp3','.flac')):
        
        return jsonify({"error": "Uploaded file is not a supported audio file"})


    try :   
        # Read the file bytes
        audio_bytes = file.read()
        # print(audio_bytes)
        
        # Store original audio (for playback)

        audio_storage[file.filename] = audio_bytes


        # Split into 3-second chunks
        chunks,sr = split_audio(audio_bytes, chunk_duration=3.0)
        
        
        print("Number of chunks:", len(chunks)) 
        for item in chunks:
            print(f"{item['time']} -> {item['audio_chunk'].shape}",flush=True)

        # emotion_r = []
        # last_e= None
        # fetch the audio to speech
        result = []
        for item in chunks:
            print("Starting transcription at", item["time"], flush=True)
            text = SC.chunk_script(item["audio_chunk"], sr)
            print("Finished transcription at", item["time"], "Text:", text, flush=True)
            result.append({
                "time": item["time"],
                "text": text
            })
            
        # emotion1 = detect_voice_emotion(text)
        # print("EMOTION:", emotion)
        
        
        # if emotion1 != last_e:
        #     emotion_r.append({
        #         "time": item["time"],
        #         "text": text,
        #         "emotion": emotion1
        #     })
        #     last_e = emotion1
        # print("FINAL EMOTION RESULTS:")
        # for e in emotion_r:
        #     print(e)
        
        
        
        
        
        
        # print(result)
        
        emotion_results = []
        last_emotion = None
        
        for item in result:
            emotion = detect_emotion(item["text"])

            if emotion != last_emotion:   # detect change
                emotion_results.append({
                    "time": item["time"],
                    "text": item["text"],
                    "emotion": emotion
                })
                last_emotion = emotion
        
        print(emotion_results)
        # Return success with a URL to play
        for i in emotion_results:
            print(i)
            
            
            
            
        return jsonify({
            "filename": file.filename,
            "play_url": f"/play/{file.filename}",
            "transcription": result,
            "emotions": emotion_results
        })

    except :
        return "file not read properly"


@upload_bp.route("/play/<filename>")
def play_audio(filename):
    if filename not in audio_storage:
        return "Audio not found", 404

    mime_type, _ = mimetypes.guess_type(filename)
    if mime_type is None:
        mime_type = "application/octet-stream"

    return send_file(
        io.BytesIO(audio_storage[filename]),
        mimetype=mime_type,
        as_attachment=False
    )