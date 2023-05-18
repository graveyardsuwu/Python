import requests, json, os, time, pyperclip
import tkinter as tk
from tkinter import messagebox
from termcolor import colored
from main import menu

# So ugly but who cares
os.system('mode 96,20')
os.system(f'title Launching Bootstrapper.py')
latestVersionURL = "https://raw.githubusercontent.com/graveyardsuwu/Python/main/LinkJoiner/version.txt"
versionName = 'version.txt'
localVersion = None

response = requests.get("https://raw.githubusercontent.com/graveyardsuwu/Python/main/LinkJoiner/download.txt")
download = response.text.strip()

binFolder = "bin"
if not os.path.exists(binFolder):
    os.makedirs(binFolder)

versionPath = os.path.join(binFolder, versionName)
localVersion = "0.0.2"
with open(versionPath, 'w') as f:
    json.dump({"version": localVersion}, f)

response = requests.get(latestVersionURL)
latestVersion = json.loads(response.text)["version"]

def printScreen(s, Width=95, Height=20):
    leftPadding = (Width - len(s)) // 2
    topPadding = Height // 4

    for _ in range(topPadding):
        print()
        
    print(' ' * leftPadding + s)

    for _ in range(topPadding):
        print()

def printProgressBar(iteration, total, length=50, fill='█', color='white', width=100):
    filledLength = int(length * iteration // total)
    bar = colored(fill * filledLength + '-' * (length - filledLength), color)

    padding = ' ' * ((width - len(bar)) // 2)

    print(f'\r{padding}{bar}', end = '\r')
    if iteration == total: 
        print()

def checkVersion():
    printScreen("Checking for Updates... ")
    printProgressBar(1, 4, length=50, width=100, color='yellow')
    os.system(f'title Checking for Updates...')

    time.sleep(2)
    
    if localVersion != latestVersion:
        os.system('cls')

        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Please Update!", "The download link has been copied to your clipboard.")
        pyperclip.copy(download)
    else:
        os.system('cls')
        
        printScreen("Version is up-to-date!")
        printProgressBar(3, 4, length=50, width=100, color='yellow')
        os.system(f'title Version is up-to-date!')

        time.sleep(1)
        launchApp()


def launchApp():
    os.system('cls')

    printScreen("Ready!", 90)
    printProgressBar(4, 4, length=50, width=100, color='yellow')
    os.system(f'title Launching...')

    time.sleep(1)

    os.system('cls')

    os.system('mode 96,40')
    menu.run()
    

if __name__ == "__main__":
    checkVersion()
