from pytubefix import YouTube, exceptions
import webbrowser
import sys
import os
import re
import ffmpeg # using ffmpeg library for dist to avoid ffmpeg system install requirement


additional_params = {
    # can add additional params here later
    '-v': 'video only',
    '-a': 'audio only',
    '-b': 'both audio and video',
    '-mp3': 'convert audio to mp3 after download',
    '-p': 'custom path for download',
    '-t': 'get thumbnail link'
    # implement mutually exclusive constraints later
}




def main():
    try:
        while True:
            user_input = input("Paste a YouTube video link here: ")
            global user_args
            user_args = user_input.split()
            # parse input params here
            # create docs
            video = validate_video_link(user_args[0])
            if video:
                break

        while True:
            if '-t' in user_args:
                webbrowser.open(get_thumbnail(video))
                break
            else:
                download_video(video)
                break

        sys.exit(0)
    except EOFError:
        print("Thanks for using this program!")
        sys.exit(0)



def validate_video_link(link):
    try:
        return YouTube(link, use_po_token=False, token_file="token.json")
    except exceptions.RegexMatchError:
        print("Please input a valid YouTube URL")
        return None


def download_video(video, type="Video", path=os.getcwd()):
    if "-p" in user_args:
        path = custom_path()
    
    if "-v" in user_args:
        stream = (
        video.streams
            .filter(adaptive=True, only_video=True, file_extension="mp4")
            .order_by("resolution")
            .desc()
            .first()
        )
        stream.download(output_path=path)
        sys.exit(0)
    
    elif "-a" in user_args:
        stream = (
            video.streams.filter(only_audio=True, mime_type="audio/mp4")
            .order_by("abr")
            .desc()
            .first()
        )
        input_path = stream.download(output_path=path)
        if "-mp3" in user_args:
            output_file = os.path.join(path, f"{safe_filename(video.title)}.mp3")
            convert_m4a_to_mp3(input_path, output_file)
            if os.path.exists(input_path):
                os.remove(input_path)
        sys.exit(0)
    
    elif "-b" in user_args:
        combine_audio_video(video, output_path=path)
        sys.exit(0)

    # print(video.streams.filter(adaptive=True, only_video=True, file_extension="mp4").order_by("resolution").desc().first())

def custom_path():
    while True:
        custom_path = input("Enter the path where you would like to save: ").strip()
        if os.path.exists(custom_path):
            return custom_path
        else:
            print("Invalid path. Please try again.")
            continue
    
def safe_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name)


def combine_audio_video(video, output_path):
    
    print("Combining audio and video...")
    

    # can use try except to handle exceptions.BotDetection
    # can try the program again with po token true or false
    # can ask user to regenerate po token
    
    audio_stream = video.streams.filter(only_audio=True, mime_type="audio/mp4").order_by("abr").desc().first()
    
    video_stream = (
    video.streams
    .filter(adaptive=True, only_video=True, file_extension="mp4")
    .order_by("resolution")
    .desc()
    .first()
    )


    if not audio_stream or not video_stream:
        print("Could not find suitable audio or video streams.")
        return

    audio_path = audio_stream.download(filename_prefix="audio_")
    video_path = video_stream.download(filename_prefix="video_")

    output_path = os.path.join(output_path, f"{safe_filename(video.title)}.mp4")
    
    video_input = ffmpeg.input(video_path)
    audio_input = ffmpeg.input(audio_path)
    
    ffmpeg.output(
        video_input, audio_input,
        output_path,
        vcodec='copy',
        acodec='copy',
        n=None
    ).run()

    # Clean up
    if os.path.exists(audio_path):
        os.remove(audio_path)
    if os.path.exists(video_path):
        os.remove(video_path)
    

def get_thumbnail(video):
    print("Thumbnail link opened in browser")
    return video.thumbnail_url

# make new function for converting m4a to mp3 if user wants mp3
# use this ffmpeg command:
# ffmpeg -i input.m4a -c:a libmp3lame -q:a 0 output.mp3

# implement this function
def convert_m4a_to_mp3(input_file, output_file):
    
    input = ffmpeg.input(input_file)
    ffmpeg.output(
        input,
        output_file,
        acodec='libmp3lame',
        **{'q:a': 0},
        n=None
    ).run()

if __name__ == "__main__":
    main()
    