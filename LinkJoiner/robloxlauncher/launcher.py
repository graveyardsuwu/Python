import requests, os,  re, time, urllib.parse, random

class RobloxLauncher:
    def __init__(self, placeId: int, cookie: str, csrfToken: str, authToken: str):
        self.placeId = placeId
        self.cookie = cookie
        self.privateLink = ""
        self.csrfToken = csrfToken
        self.authToken = authToken

    def parseAccessCode(self, response):
        code = ""
        match = re.search("Roblox.GameLauncher.joinPrivateGame\\(\\d+\\,\\s*'(\w+\-\w+\-\w+\-\w+\-\w+)'", response.text)

        if match and len(match.groups()) == 1:
            code = match.group(1)
            return code
        
        return False

    def startRoblox(self, link):
        try:
            self.privateLink = link

            linkCode = re.search("privateServerLinkCode=(.+)", self.privateLink).group(1) if "privateServerLinkCode=" in self.privateLink else ""
            
            if linkCode:
                url = f"https://www.roblox.com/games/{self.placeId}?privateServerLinkCode={linkCode}"
                response = requests.get(url, cookies={".ROBLOSECURITY": self.cookie}, headers={"X-CSRF-TOKEN": self.csrfToken, "Referer": url})
                if response.status_code == 200:
                    accessCode = self.parseAccessCode(response)

            ticket = self.authToken.headers['rbx-authentication-ticket']

            print("Fetching Access")
            print("\nStarting ROBLOX... ")

            browserTrackerId = str(random.randint(100000, 175000)) + str(random.randint(100000, 900000))
            timestamp = '{0:.0f}'.format(round(time.time() * 1000))

            url = urllib.parse.quote(f'https://assetgame.roblox.com/game/PlaceLauncher.ashx?request=RequestPrivateGame&browserTrackerId={browserTrackerId}&placeId={self.placeId}&accessCode={accessCode}&isPlayTogetherGame=false+browsertrackerid:147062882894+robloxLocale:en_us+gameLocale:en_us+channel:')
            command = f"roblox-player:1+launchmode:play+gameinfo:{ticket}+launchtime:{timestamp}+placelauncherurl:{url}"
            os.startfile(command)

        except Exception as e:

            print(f"Error: {e}")
