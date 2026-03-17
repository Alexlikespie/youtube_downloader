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

# remove path option and instead allow user to update the default path


def main():
    try:
        while True:
            global user_args
            user_input = input("Paste a YouTube video link here: ")
            user_args = user_input.split()
            if "-mp3" in user_args and "-a" not in user_args:
                print("The -mp3 option requires the -a option. Please include -a if you want to convert to mp3.")
                continue
            if "-t" in user_args and any(opt in user_args for opt in ["-v", "-a", "-b"]):
                print("The -t option cannot be used with -v, -a, or -b. Please choose either to get the thumbnail or to download the video/audio.")
                continue
            # apparently bools can be counted
            if ("-v" in user_args) + ("-a" in user_args) + ("-b" in user_args) > 1:
                print("Please choose only one of the following options: -v, -a, or -b.")
                continue
            # parse input params here
            # create docs
            video = validate_video_link(user_args[0])
            if video:
                video.register_on_progress_callback(on_progress)
                # if "-b" not in user_args or len(user_args) > 1:
                #     video.register_on_complete_callback(on_complete)
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
        # creates a path and then checks if it exists
        # indexes filenames if it already exists
        video_path = os.path.join(path, f"{safe_filename(video.title)}.mp4")
        video_path = unique_filename(video_path)
        print("Downloading file...")
        stream.download(output_path=path, filename=os.path.basename(video_path))
        print("\nDownload Complete!")
        sys.exit(0)
    
    elif "-a" in user_args:
        stream = (
            video.streams.filter(only_audio=True, mime_type="audio/mp4")
            .order_by("abr")
            .desc()
            .first()
        )
        audio_path = os.path.join(path, f"{safe_filename(video.title)}.m4a")
        audio_path = unique_filename(audio_path)
        print("Downloading file...")
        input_file = stream.download(output_path=path, filename=os.path.basename(audio_path))
        if "-mp3" in user_args:
            output_file = os.path.join(path, f"{safe_filename(video.title)}.mp3")
            output_file = unique_filename(output_file)
            convert_m4a_to_mp3(input_file, output_file)
            if os.path.exists(input_file):
                os.remove(input_file)
        else:
            print("\nDownload Complete!")
        sys.exit(0)
    
    elif "-b" in user_args:
        combine_audio_video(video, output_path=path)
        sys.exit(0)
        
    else:
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
    name = re.sub(r'[\\/*?:"<>|]', "", name)   # remove illegal characters
    name = name.strip().rstrip(".")            # remove trailing spaces/periods

    reserved = {
        "CON","PRN","AUX","NUL",
        "COM1","COM2","COM3","COM4","COM5","COM6","COM7","COM8","COM9",
        "LPT1","LPT2","LPT3","LPT4","LPT5","LPT6","LPT7","LPT8","LPT9"
    }

    if name.upper() in reserved:
        name = "_" + name

    return name

def unique_filename(path):
    base, ext = os.path.splitext(path)
    counter = 1

    while os.path.exists(path):
        path = f"{base} ({counter}){ext}"
        counter += 1

    return path


def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percent = bytes_downloaded / total_size * 100

    # Simple text progress bar
    bar_length = 40
    filled_length = int(bar_length * bytes_downloaded // total_size)
    bar = "█" * filled_length + "-" * (bar_length - filled_length)

    sys.stdout.write(f"\r[{bar}] {percent:6.2f}%")
    sys.stdout.flush()
    
def on_complete(stream, file_path):
    # This runs **once** after the download finishes
    print("\nDownload Complete!")

def combine_audio_video(video, output_path):    

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

    print("Downloading Audio...")
    audio_path = audio_stream.download(filename_prefix="audio_")
    print("\nAudio Complete!")
    print("Downloading Video...")
    video_path = video_stream.download(filename_prefix="video_")
    print("\nVideo Complete!")

    output_path = os.path.join(output_path, f"{safe_filename(video.title)}.mp4")
    output_path = unique_filename(output_path)
    
    video_input = ffmpeg.input(video_path)
    audio_input = ffmpeg.input(audio_path)
    
    print("Combining audio and video...")
    
    ffmpeg.output(
        video_input, audio_input,
        output_path,
        vcodec='copy',
        acodec='copy',
        n=None
    ).run(quiet=True)
    
    print("Download Complete!")

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
    
    output_file = unique_filename(output_file)
    
    ffmpeg.output(
        input,
        output_file,
        acodec='libmp3lame',
        **{'q:a': 0},
        n=None
    ).run(quiet=True)
    
    print("\nDownload Complete!")

if __name__ == "__main__":
    main()
    
    