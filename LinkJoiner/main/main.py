import requests, os,  pathlib, json, time
from monitor.monitor import ChannelMonitor
from robloxlauncher.launcher import RobloxLauncher
from main import menu

class RobloxUpdater:
    def __init__(self, cookie):
        self.cookie = cookie

    def checkVersion(self):
        print("\033[38;5;208m[*]\033[0m Checking Roblox... ", end="")
        # Broken, was causing issues with compiling, will fix soon ;-;
        print("100%")

    def fetchCsrfToken(self):
        print("\033[38;5;208m[*]\033[0m Fetching CSRF Token...", end="")

        tokenUrl = "https://auth.roblox.com/v1/authentication-ticket"
        req = requests.post(tokenUrl, headers={"Cookie": ".ROBLOSECURITY=" + self.cookie})

        if 'x-csrf-token' in req.headers:
            csrfToken = req.headers['x-csrf-token']
            print("100%")
            return csrfToken
        else:
            print("\n\033[38;5;196m[*]\033[0m Error: Incorrect Roblox Token, remove /bin/credentials.json and re-launch.")
            time.sleep(5)
            menu.run()

        
    def fetchAuthToken(self, csrfToken):
        print("\033[38;5;208m[*]\033[0m Fetching Auth Token...", end="")

        tokenUrl = "https://auth.roblox.com/v1/authentication-ticket"
        headers = {
            "Cookie": ".ROBLOSECURITY=" + self.cookie,
            "Origin": "https://www.roblox.com",
            "Referer": "https://www.roblox.com/",
            "X-CSRF-TOKEN": csrfToken
        }

        print("100%")

        return requests.post(tokenUrl, headers=headers)

def run():
    credPath = 'bin/credentials.json'
    retries = 3
    delay = 0.1

    for _ in range(retries):
        try:
            with open(credPath, 'r') as f:
                credentials = json.load(f)
            break
        except (FileNotFoundError, json.JSONDecodeError):
            time.sleep(delay)
            delay *= 2
    else:
        print("\n\033[38;5;196m[*]\033[0m Error: Incorrect Roblox Token, remove /bin/credentials.json and re-launch.")
        return

    robloxToken = credentials.get("RobloxToken")
    placeId = 2788229376
    discordToken = credentials.get("DiscordToken")
    discordChannelId = credentials.get("DiscordChannelId")

    if not robloxToken or not discordToken or not discordChannelId:
        print("Error: Incomplete credentials.")
        return

    robloxToken = credentials["RobloxToken"]
    placeId = 2788229376
    discordToken = credentials["DiscordToken"]
    discordChannelId = credentials["DiscordChannelId"]

    robloxUpdater = RobloxUpdater(robloxToken)
    robloxUpdater.checkVersion()
    csrfToken = robloxUpdater.fetchCsrfToken()
    authToken = robloxUpdater.fetchAuthToken(csrfToken)

    robloxLauncher = RobloxLauncher(placeId, robloxToken, csrfToken, authToken)

    ChannelMonitor(discordChannelId, discordToken, robloxLauncher)

