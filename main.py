from pytubefix import YouTube, exceptions
import webbrowser
import sys
# from moviepy import VideoFileClip, AudioFileClip
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
                    )

            action = choice(user_action)
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
        return YouTube(link)
    except exceptions.RegexMatchError:
        print("Please input a valid YouTube URL")
        return None


def choice(choice):
    while True:
        if choice.strip() == "1":
            return "1"
        elif choice.strip() == "2":
            return "2"
        else:
            print("Please input either 1 or 2")
            continue




def download_video(video):
    while True:
        format = input(
            " Video only, audio only, or both? \n"
            " (1/2/3): ").strip()
        if format == "1" or format == "2" or format == "3":
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
        if path == "1" or path == "2":
            break
        else:
            print("Please input either 1 or 2")
            continue
        
    if format == "1":
        stream = (
            video.streams.filter(file_extension="mp4")
            .order_by("resolution")
            .desc()
            .first()
            )
        if path == "1":
            stream.download()
        elif path == "2":
            while True:
                custom_path = input("Enter the path where you would like to save: ").strip()
                try:
                    stream.download(custom_path)
                    break
                except Exception:
                    print("Invalid path. Please try again.")
                    continue
    elif format == "2":
        stream = video.streams.filter(only_audio=True).first()
        if path == "1":
            stream.download()
        elif path == "2":
            while True:
                custom_path = input("Enter the path where you would like to save: ").strip()
                try:
                    stream.download(custom_path)
                    break
                except Exception:
                    print("Invalid path. Please try again.")
                    continue
    elif format.strip() == "3":
        if path == "1":
            combine_audio_video(video)
        elif path == "2":
            # TODO
            pass

    print("Download Complete!")
    
    
def safe_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name)


def combine_audio_video(video, path=os.getcwd()):
    
    print("Combining audio and video...")
    audio_stream = video.streams.filter(only_audio=True).first()
    video_stream = video.streams.filter(file_extension="mp4").order_by("resolution").desc().first()

    if not audio_stream or not video_stream:
        print("Could not find suitable audio or video streams.")
        return

    audio_path = audio_stream.download(filename_prefix="audio_")
    video_path = video_stream.download(filename_prefix="video_")

    output_path = os.path.join(path, f"{safe_filename(video.title)}.mp4")
    
    try:
        # Build FFmpeg command
        command = [
            "ffmpeg",
            "-i", video_path,
            "-i", audio_path,
            "-c:v", "copy",
            "-c:a", "aac",
            "-strict", "experimental",
            "-y",  # Overwrite output if it exists
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

if __name__ == "__main__":
    main()