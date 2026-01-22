from PIL import Image, ImageSequence
import time
import os
import shutil
import argparse

def pixelToAcii(pixel):
    aciiChar = "@%#*+=-:. "
    index = int((pixel / 255) * (len(aciiChar) - 1))
    return aciiChar[index]


def getTerminalSize():
    size = shutil.get_terminal_size()
    return size.columns, size.lines - 2


def playGifAcii(img):
    try:
        duration = img.info.get('duration', 100) / 1000.0
        print("\033[?25l", end="")  # Hide cursor
        while True:
            for frame in ImageSequence.Iterator(img):
                termWidth, termHeight = getTerminalSize()
                print("\033[H", end="")  # Move cursor to top
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
        print("\033[?25h")  # Show cursor again
        print("\nGIF Playback Stopped.")
        return


def imageToAcii(path):
    try:
        img = Image.open(path)
    except FileNotFoundError:
        print(f"Error: File '{path}' does not exist.")
        return
    except Exception as e:
        print(f"Error: Could not open file. {str(e)}")
        return
    
    # Clear terminal for art
    os.system("cls" if os.name == "nt" else "clear")
    
    if img.format == "GIF":
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


def main():
    os.system("cls" if os.name == "nt" else "clear")
    """Entry point for the command-line tool."""
    parser = argparse.ArgumentParser(
        description='Convert images and GIFs to ASCII art',
        epilog='Example: giftwoascii path/to/image.png'
    )
    
    parser.add_argument(
        'path',
        nargs='?',  # Makes it optional
        default=None,
        help='Path to the image or GIF file'
    )
    
    args = parser.parse_args()
    
    # Check if user provided a path
    if args.path is None:
        print("Usage: giftwoascii <path-to-image>")
        print("Example: giftwoascii myimage.png")
        parser.print_help()
        return
    
    # Process the image
    imageToAcii(args.path)

if __name__ == "__main__":
    main()