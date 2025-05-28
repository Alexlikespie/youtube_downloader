# YouTube Downloader and Thumbnail Retriever

#### Video Demo: <https://youtu.be/mIOGcGXgNoE>


## Overview

YouTube Downloader and Thumbnail Retriever is a Python program that does exactly that; it takes in a YouTube link and gives back the thumbnail or downloads the video to your computer. When the script is run, the user will be prompted for a valid YouTube link. They will then be asked if they would like to download the video or retrieve the thumbnail. If the former is chosen, they will then again be prompted for if they would like to download the video as an `MP4` file or just the audio as an `M4A` file, as well as where they would like to save it. If the latter is chosen, the thumbnail of the requested video will be opened in their web browser, where the user can download or copy the image from there.

## How to Use

When a user first runs `project.py`, they will be prompted for a valid YouTube URL. If an invalid URL is inputted, the user will be repromoted until a valid URL is given. Then, the user will be asked if they would like to download the video or retrieve the thumbnail, in which the user would then input either `1` or `2` respectively. If `2` is inputted, the thumbnail for the requested video will be opened in the user's browser and the program would exit. If `1` is inputted, the user will then again be prompted for whether they would like to download the video or just the audio by then inputting `1` or `2` respectively. After the user makes their choice, they then will be prompted on whether they would like to save their download in the current folder (the folder in which `project.py` exists), or if they would like to save the project somewhere else by inputting `1` or `2` respectively. If they choose the latter, they will then be prompted for a path in which the video should be downloaded to. Once the user inputs their desired path, the video will be downloaded and the project will exit.

## What Each File Contains

### `project.py`

#### This file is the main `.py` file of the project. It contains all of my code that makes this project work.

### `test_project.py`

#### This file contains the tests to 3 of the functions used in `project.py`. These tests can be executed with `pytest`.

### `requirements.txt`

#### This file contains all of the `pip` installable packages/libraries required for the project to work properly.

## Design Choices

When designing the layout and logic of my code, there were many aspects in which I had trouble deciding how to implement. At first, I used `tkinter` to create a `gui` for the project, as I believed it would make the project more accessible and aesthetically pleasing. However through the development process, I realized how unnecessary a `gui` would be for this type of small project, and I ended up scrapping that idea, instead opting for a more traditional approach in which the program simply runs in the terminal window.

Another dilemma I encountered was what responsibility I should give each function. At first I made every function do their full job, including a side effect, and only defined a `main()` function to call each other function. The reason that I first approached this project with this logic is that it was the easiest for me to write and simplest logic for me to understand. However, I ended up changing the logic and responsibility of each function because it is not deemed as a best practice to allow every function to have a side effect. My previous logic also prevented me from easily creating tests for my functions, as they now required mocking. So, I ended up changing the logic of my functions as to provide a return value to `main()`, and then let `main()` do the printing/downloading. I also reassigned the various uses of the `input()` function to `main()` as well, so that I could provide an argument to each of the other functions, further making them easier to write tests for without mocking.

## Final Thoughts

Overall, the YouTube Downloader and Thumbnail Retriever was my first ever proper programming project, and I had a great deal of fun and learned a lot in the process. I hope that whoever's reading this makes use of my project and that it helps to add productivity to your workflow, even if it's only minimal.
