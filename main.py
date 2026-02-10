from pytubefix import YouTube, exceptions
import webbrowser
import sys
import os
import re
import subprocess

def main():
    try:
        while True:
            link = input("Paste a YouTube video link here: ")
            video = validate_video_link(link)
            if video:
                break

        while True:
            user_action = input(
                    " What would you like to do with the video? \n"
                    " Download it? (1) \n"
                    " Get the Thumbnail Link? (2) \n"
                    " (1/2): "
                    ).strip()
            if user_action not in ["1", "2"]:
                print("Please input either 1 or 2")
                continue

            action = user_action
            if action == "1":
                download_video(video)
                break
            elif action == "2":
                webbrowser.open(get_thumbnail(video))
                break
            else:
                continue

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


def download_video(video):
    while True:
        format = input(
            " Video only, audio only, or both? \n"
            " (1/2/3): ").strip()
        if format in ["1", "2", "3"]:
            break
        else:
            print("Please input either 1, 2, or 3")
            continue

    while True:
        path = input(
            " Where would you like to save this download? \n"
            " In the current directory? (1) \n"
            " Somewhere else? (2) \n"
            " (1/2): "
            ).strip()
        if path in ["1", "2"]:
            break
        else:
            print("Please input either 1 or 2")
            continue
        
    if format == "1":
        stream = (
        video.streams
            .filter(adaptive=True, only_video=True, file_extension="mp4")
            .order_by("resolution")
            .desc()
            .first()
        )
        if path == "1":
            stream.download()
        elif path == "2":
            stream.download(output_path=custom_path())
            
    elif format == "2":
        stream = video.streams.filter(only_audio=True, mime_type="audio/mp4").order_by("abr").desc().first()
        if path == "1":
            stream.download()
        elif path == "2":
            stream.download(output_path=custom_path())
        # can implement a feature to convert the audio to mp3 after downloading?
        # use ffmpeg command
        # ffmpeg -i input.m4a -c:v copy -c:a libmp3lame -q:a [0-9 quality 0 highest 9 lowest] output.mp3

            
    elif format == "3":
        if path == "1":
            combine_audio_video(video)
        elif path == "2":
            combine_audio_video(video, path=custom_path())
            

    print("Download Complete!")
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


def combine_audio_video(video, path=os.getcwd()):
    
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

    output_path = os.path.join(path, f"{safe_filename(video.title)}.mp4")
    
    try:
        # Build FFmpeg command
        '''command = [
            "ffmpeg",
            "-i", video_path,
            "-i", audio_path,
            "-c:v", "copy",
            "-c:a", "aac",
            "-strict", "experimental",
            "-y",  # Overwrite output if it exists
            output_path
        ]'''
        
        command = [
            "ffmpeg",
            "-i", video_path,
            "-i", audio_path,
            "-c:v", "copy",
            "-c:a", "copy",  # No re-encoding
            "-y",
            output_path
        ]

        subprocess.run(command, check=True)

        print(f"Combined video saved to {output_path}")

    except subprocess.CalledProcessError as e:
        print(f"FFmpeg failed: {e}")

    finally:
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
    command = [
        "ffmpeg",
        "-i", input_file,
        "-c:a", "libmp3lame",
        "-q:a", "0",
        output_file
    ]
    subprocess.run(command, check=True)

if __name__ == "__main__":
    main()
    
