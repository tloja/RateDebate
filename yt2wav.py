from __future__ import unicode_literals
import yt_dlp
import ffmpeg
import sys
import os
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'wav',
    }],
}
ydl = yt_dlp.YoutubeDL(ydl_opts)

def convert_video(url):
    """
    Download the YouTube video into .wav and convert it to mono
    """
    try:
        info_dict = ydl.extract_info(url, download=True)
    except yt_dlp.utils.DownloadError:
        print(f"yt_dlp.utils.DownloadError detected, maybe check the URL?")
        exit()
    print('*' * 50)
    file_name = ydl.prepare_filename(info_dict)
    root, ext = os.path.splitext(file_name)
    wav_file = root + '.wav'
    wav_mono_file = root + '_mono.wav'
    stream = ffmpeg.input(wav_file)
    stream = ffmpeg.output(stream, wav_mono_file, ac=1).run()
    return wav_mono_file

