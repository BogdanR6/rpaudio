import sys
import os
from moviepy.audio.fx.audio_fadein import audio_fadein
from moviepy.audio.fx.audio_fadeout import audio_fadeout
from moviepy.audio.fx.audio_loop import audio_loop
from moviepy.editor import VideoFileClip, AudioFileClip

def process_video(video_file_name, audio):
    print(f'Processing {video_file_name}...')
    
    video = VideoFileClip(video_file_name)
    
    # Trim or loop the audio to match the video duration
    new_audio = audio.subclip(0, video.duration)
    new_audio = audio_loop(new_audio, duration=video.duration)
    
    # Apply fade-in and fade-out
    new_audio = audio_fadein(new_audio, 2)
    new_audio = audio_fadeout(new_audio, 2)
    
    video_with_new_audio = video.set_audio(new_audio)
    
    video_file_base_name, file_extension = os.path.splitext(video_file_name)
    output_file_name = f"{video_file_base_name}_edited{file_extension}"
    
    # Choose correct codec based on file format
    codec = "prores_ks" if file_extension.lower() == ".mov" else "libx264"
    audio_codec = "pcm_s16le" if file_extension.lower() == ".mov" else "aac"
    
    video_with_new_audio.write_videofile(output_file_name, codec=codec, audio_codec=audio_codec)
    
    video.close()

def get_video_files_from_folder(folder_path):
    supported_extensions = {".mp4", ".mov", ".avi", ".mkv", ".flv", ".wmv"}
    return [
        os.path.join(folder_path, f) for f in os.listdir(folder_path)
        if os.path.splitext(f)[1].lower() in supported_extensions
    ]

def main():
    if len(sys.argv) < 3:
        print("Usage: python rpaudio.py <audio_file> <video_file/folder>")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    target_path = sys.argv[2]
    
    if not os.path.exists(audio_file):
        print(f"Error: Audio file '{audio_file}' not found.")
        sys.exit(1)
    
    audio = AudioFileClip(audio_file)
    
    if os.path.isdir(target_path):
        video_files = get_video_files_from_folder(target_path)
        if not video_files:
            print("Error: No compatible video files found in the folder.")
            sys.exit(1)
        for video_file in video_files:
            process_video(video_file, audio)
    elif os.path.isfile(target_path):
        process_video(target_path, audio)
    else:
        print(f"Error: '{target_path}' is neither a valid file nor a folder.")
        sys.exit(1)

if __name__ == "__main__":
    main()
