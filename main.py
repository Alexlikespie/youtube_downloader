from pytubefix import YouTube, exceptions
import webbrowser
import sys
import moviepy
import os

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

        sys.exit(1)
    except EOFError:
        print("Thanks for using this program!")
        sys.exit(1)



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
            return None




def download_video(video):
    stream = (
        video.streams.filter(file_extension="mp4")
        .order_by("resolution")
        .desc()
        .first()
        )

    while True:
        format = input(
            " Video only or audio only? \n"
            " (1/2): ")
        if format.strip() == "1":
            break
        elif format.strip() == "2":
            stream = video.streams.filter(only_audio=True).first()
            break
        else:
            print("Please input either 1 or 2")
            continue

    while True:
        path = input(
            " Where would you like to save this download? \n"
            " In the current directory? (1) \n"
            " Somewhere else? (2) \n"
            " (1/2): "
            )

        if path == "1":
            combine_audio_video(video)
            # stream.download()
            break
        elif path == "2":
            custom_path = input("Enter the path where you would like to save: ")
            try:
                stream.download(custom_path)
            except Exception:
                print("Invalid path. Please try again.")
                continue
            break
        else:
            print("Please input either 1 or 2")

    print("Download Complete!")

def combine_audio_video(video):
    video_stream = stream = (
        video.streams.filter(file_extension="mp4")
        .order_by("resolution")
        .desc()
        .first()
        )
    audio_stream = video.streams.filter(only_audio=True).first()
    video_stream.download()
    audio_stream.download()
    

def get_thumbnail(video):
    print("Thumbnail link opened in browser")
    return video.thumbnail_url

if __name__ == "__main__":
    main()