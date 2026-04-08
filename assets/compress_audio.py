import os
try:
    from pydub import AudioSegment
    import imageio_ffmpeg as ffmpeg
except ImportError:
    print("Error: Missing dependencies. Please run: pip install pydub imageio-ffmpeg")
    exit(1)

# Configure pydub to use the ffmpeg binary from imageio-ffmpeg
AudioSegment.converter = ffmpeg.get_ffmpeg_exe()

def compress_wav_to_mp3(wav_path, bitrate="192k"):
    if not os.path.exists(wav_path):
        print(f"File not found: {wav_path}")
        return
    
    mp3_path = os.path.splitext(wav_path)[0] + ".mp3"
    print(f"Compressing {wav_path} to {mp3_path} at {bitrate}...")
    
    try:
        audio = AudioSegment.from_wav(wav_path)
        audio.export(mp3_path, format="mp3", bitrate=bitrate)
        print(f"Done! New file size: {os.path.getsize(mp3_path) / 1024 / 1024:.2f} MB")
        return mp3_path
    except Exception as e:
        print(f"Error compressing {wav_path}: {e}")
        return None

if __name__ == "__main__":
    tracks = [
        "assets/music/comingHome/ComingHomeFinal.wav",
        "assets/music/leapSolar/beach song_voicemail.wav",
        "assets/music/leapSolar/car wash.wav"
    ]
    
    for track in tracks:
        # Check relative paths based on script location or absolute paths
        # Assuming script runs from root
        compress_wav_to_mp3(track)
