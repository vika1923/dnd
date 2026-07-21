import queue
import sys
import threading
from faster_whisper import WhisperModel
import numpy as np
import sounddevice as sd

# Configuration Constants
# Whisper natively expects 16000Hz audio sample rate
SAMPLE_RATE = 16000
# Duration of each audio block chunk in seconds
BLOCK_DURATION = 1.0
# Number of audio frames per block chunk
BLOCK_SIZE = int(SAMPLE_RATE * BLOCK_DURATION)

# Thread-safe queue to pass audio chunks from recording thread to processing thread
audio_queue = queue.Queue()

def record_audio_callback(indata, frames, time, status):
    """Callback function executed by sounddevice for each audio block."""
    if status:
        print(status, file=sys.stderr)
    # Convert input data to 32-bit floating point and push to queue
    audio_queue.put(indata.copy().flatten())

def transcription_worker(model_size="tiny"):
    """Worker thread that pulls audio from the queue and transcribes it."""
    print(f"Loading Whisper model '{model_size}'...")
    # Use 'cuda' instead of 'cpu' if you have a compatible NVIDIA GPU configured
    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    print("Model loaded. Speak into your microphone now...")

    # Maintain an audio buffer to preserve context across rolling chunks
    audio_buffer = np.array([], dtype=np.float32)

    while True:
        try:
            # Grab audio chunk from queue (blocks if queue is empty)
            chunk = audio_queue.get()
            audio_buffer = np.append(audio_buffer, chunk)

            # Limit buffer size to last 5 seconds to manage memory & processing latency
            max_buffer_len = SAMPLE_RATE * 5
            if len(audio_buffer) > max_buffer_len:
                audio_buffer = audio_buffer[-max_buffer_len:]

            # Transcribe the rolling audio buffer
            # beam_size=1 enforces fastest decoding speed
            segments, info = model.transcribe(audio_buffer, beam_size=1)

            # Clear the current console line and print real-time updates
            sys.stdout.write("\r")
            for segment in segments:
                sys.stdout.write(f"[{segment.start:.1f}s -> {segment.end:.1f}s]: {segment.text} ")
            sys.stdout.flush()

            audio_queue.task_done()
        except KeyboardInterrupt:
            break

def main():
    # Start the transcription engine in a background daemon thread
    # Use "tiny" or "base" for optimal speed; "small" or "medium" for accuracy
    threading.Thread(target=transcription_worker, args=("tiny",), daemon=True).start()

    # Open microphone input stream and stream continuous raw audio chunks
    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, callback=record_audio_callback, blocksize=BLOCK_SIZE):
        print("Microphone pipeline active. Press Ctrl+C to terminate.")
        try:
            while True:
                sd.sleep(100)
        except KeyboardInterrupt:
            print("\nExiting live transcription program...")

if __name__ == "__main__":
    main()
