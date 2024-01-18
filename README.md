
# UHC Video Maker

This project aims to increase the fidelity of gameplay when watching compatible minecraft Ultra Hardcore from known Youtubers.

Although this program was made to function around the "ElRichMC" hispanic UHC series, there is no reason adapting it to any other format wouldn't be possible.

## Features

- Timer-based synchronization of videos
- Downloads all the videos from a playlist
- Automatic video arranging for ffmpeg outputs

## Dependencies

Included in the repository is the requirements.txt file that included most of what you need to run the application.

Required is also the following pytesseract data:

- https://github.com/xHayden/Minecraft-OCR

Make sure the .traineddata is located in the proper directory.

**Windows:** C:\Users\USER\AppData\Local\Tesseract-OCR\tessdata

**Linux:** /usr/local/share/tessdata

*These paths are what I've used in my experience, in the event something fails, I would make sure these paths are correct.*

## Roadmap

- Add support for videos with breaks throughout the duration of the episodes.
- Add support for any resolution other than 720p.
- Add support for frame rates other than 30 or lower.
- Integrate video-downloader into the main program.
- Create a GUI for easy of use.
- Enable video rearrange.
- Enable multi-channel audio selection in real-time.
- Optimize OCR stage.

