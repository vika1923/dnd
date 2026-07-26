import whisper

model = whisper.load_model("large-v3")


def transcribe(audio_path):
    audio = whisper.load_audio(audio_path)
    return model.transcribe(audio, fp16=False, language='English')["text"]


if __name__ == "__main__": 
    # print(transcribe("audio/test.mp3"))
    print(whisper.available_models())