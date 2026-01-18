from PIL import Image, ImageSequence
import time
import os
import shutil

#clears terminal for art
os.system("cls" if os.name == "nt" else "clear")

imgPath = input(": ")

aciiChar = "@%#*+=-:. "

# converts pixel brightness (0-255) to ACII character
def pixelToAcii(pixel):
    index = int((pixel / 255) * (len(aciiChar) - 1))
    return aciiChar[index]

def getTerminalSize():
    size = shutil.get_terminal_size()
    return size.columns, size.lines - 2

def playGifAcii(img):
    try:
        duration = img.info.get('duration', 100) / 1000.0

        print("\033[?25l", end="")

        while True:
            for frame in ImageSequence.Iterator(img):
                termWidth, termHeight = getTerminalSize()

                print("\033[H", end="")
                frame = frame.convert("L")

                imgWidth, imgHeight = frame.size
                aspectRatio = imgWidth / imgHeight

                targetWidth = min(termWidth, int(termHeight * aspectRatio * 2))
                targetHeight = int(targetWidth / aspectRatio / 2)

                if targetHeight > termHeight:
                    targetHeight = termHeight
                    targetWidth = int(targetHeight * aspectRatio * 2)

                frame = frame.resize((targetWidth, targetHeight))
                pixels = frame.load()

                art = ""

                for y in range(frame.height):
                    for x in range(frame.width):
                        pixel = pixels[x, y]
                        char = pixelToAcii(pixel)
                        art += char
                    art += "\n"
                
                print(art, end="", flush=True)
                time.sleep(duration)

    except KeyboardInterrupt:
        print("\033[?25h")
        print("\nGIF Playback Stopped.")
        return


def imageToAcii(path):
    try:
        img = Image.open(path)
    except FileNotFoundError:
        print("File Does Not Exist Or Found.")
        return #or ask again
    except TypeError:
        print("Inappropriate File Type Or Unsupported File.")
        return #or ask again

    if (img.format == "GIF"):
        playGifAcii(img)

    else:
        termWidth, termHeight = getTerminalSize()
        
        img = img.convert("L")
        imgWidth, imgHeight = img.size
        aspectRatio = imgWidth / imgHeight
        
        targetWidth = min(termWidth, int(termHeight * aspectRatio * 2))
        targetHeight = int(targetWidth / aspectRatio / 2)
        
        if targetHeight > termHeight:
            targetHeight = termHeight
            targetWidth = int(targetHeight * aspectRatio * 2)
        
        img = img.resize((targetWidth, targetHeight))
        pixels = img.load()
        
        art = ""
        for y in range(img.height):
            for x in range(img.width):
                pixel = pixels[x, y]
                char = pixelToAcii(pixel)
                art += char
            art += "\n"
        
        print(art)

    
    return


imageToAcii(imgPath)