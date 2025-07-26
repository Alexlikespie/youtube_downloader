from pytubefix import YouTube

yt = YouTube("https://www.youtube.com/watch?v=jGztGfRujSE", use_po_token="True", token_file="token.json")
print(yt.title)
