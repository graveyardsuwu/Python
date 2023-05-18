import os, json, time
from os import system
from main import main

text = """

   __         __     __   __     __  __          __     ______     __     __   __     ______     ______    
  /\ \       /\ \   /\ "-.\ \   /\ \/ /         /\ \   /\  __ \   /\ \   /\ "-.\ \   /\  ___\   /\  == \   
  \ \ \____  \ \ \  \ \ \-.  \  \ \  _"-.      _\_\ \  \ \ \/\ \  \ \ \  \ \ \-.  \  \ \  __\   \ \  __<   
   \ \_____\  \ \_\  \ \_\\"\_\  \ \_\ \_\    /\_____\  \ \_____\  \ \_\  \ \_\\"\_\  \ \_____\  \ \_\ \_\ 
    \/_____/   \/_/   \/_/ \/_/   \/_/\/_/    \/_____/   \/_____/   \/_/   \/_/ \/_/   \/_____/   \/_/ /_/ 
                                                                                                         
"""
def orange(text):
    return "\033[38;5;208m" + text + "\033[0m"

# Credits https://github.com/venaxyt/fade/tree/main:
def fadeFire(text):
    system(""); faded = ""
    green = 250
    for line in text.splitlines():
        faded += (f"\033[38;2;255;{green};0m{line}\033[0m\n")
        if not green == 0:
            green -= 25
            if green < 0:
                green = 0
    return faded

def printToken(token, chars=6):
    return token[:chars] + '*' * 15

def loginInfo():
    if os.path.exists("bin/credentials.json"):
        with open("bin/credentials.json", 'r') as f:
            credentials = json.load(f)

            print("\n\033[38;5;208m[*]\033[0m Login Found!\n\n\033[38;5;208m------------------------------\033[0m\n")
            
            robloxToken = credentials["RobloxToken"]
            discordToken = credentials["DiscordToken"]
            discordChannelId = credentials["DiscordChannelId"]
            
            print(f"[Roblox Token] {printToken(robloxToken)}...")
            print(f"[Discord Token] {printToken(discordToken)}...")
            print(f"[Channel ID] {discordChannelId}\n")

            time.sleep(1)
            
            main.run()
    else:
        credentials = {
            "RobloxToken": input("[\033[38;5;208m*]\033[0m Enter your Roblox token: "),
            "DiscordToken": input("[\033[38;5;208m*]\033[0m Enter your Discord token: "),
            "DiscordChannelId": input("[\033[38;5;208m*]\033[0m Enter a Discord Channel ID: ")
        }

        with open("bin/credentials.json", "w") as f:
            json.dump(credentials, f)
            main.run()

        return False
    
def menuLoop():
    while True:
        os.system("cls")

        print(fadeFire(text))
        print("[1] Login".center(106).replace("1", orange("1")))
        option2 = "[2] Update".replace("2", orange("2"))
        option3 = "[3] Close".replace("3", orange("3"))

        totalSpacing = 80 - len(option2) - len(option3)
        spacing = totalSpacing // 2
        line = option2 + ' ' * spacing + option3

        print("\n")
        print(line.center(134))
        print("\n")
        
        choice = input("\033[38;5;208mOption: ")

        if choice == "1":
            loginInfo()
        elif choice == "2":
            print("Soon.")
        elif choice == '3':
            os.kill(os.getpid(), 9)
        else:
            return

def run():
    os.system("mode 108,30")
    os.system("title Link Joiner - suley#0001")
    menuLoop()
