import sys
import os
from moviepy.audio.fx.audio_fadein import audio_fadein
from moviepy.audio.fx.audio_fadeout import audio_fadeout
from moviepy.audio.fx.audio_loop import audio_loop
from moviepy.editor import VideoFileClip, AudioFileClip

audio = AudioFileClip(sys.argv[1])

for video_file_name in sys.argv[2:]:
    print(f'Processing {video_file_name}...')

    video = VideoFileClip(video_file_name)

    # Trim or loop the audio to match the video duration
    new_audio = audio.subclip(0, video.duration)
    new_audio = audio_loop(new_audio, duration=video.duration)

    # Apply fadein and fadeout
    new_audio = audio_fadein(new_audio, 2)
    new_audio = audio_fadeout(new_audio, 2)

    # Replace the video's audio with the new audio
    video_with_new_audio = video.set_audio(new_audio)

    # Preserve the original format
    video_file_base_name, file_extension = os.path.splitext(video_file_name)
    output_file_name = f"{video_file_base_name}_edited{file_extension}"

    # Choose correct codec based on file format
    codec = "prores_ks" if file_extension.lower() == ".mov" else "libx264"
    audio_codec = "pcm_s16le" if file_extension.lower() == ".mov" else "aac"

    video_with_new_audio.write_videofile(output_file_name, codec=codec, audio_codec=audio_codec)

    video.close()