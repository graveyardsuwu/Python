import requests, re
from datetime import datetime
from dateutil.parser import parse
from dateutil.tz import tzutc

class ChannelMonitor:
    session = requests.Session()

    def __init__(self, id, token, robloxLauncher):
        self.id = id
        self.url = f"https://discord.com/api/v9/channels/{id}/messages?limit=5"
        self.token = token
        self.headers = {
            "authorization": self.token
        }
        self.delay = 0.5  # Leave as 0.5, could cause rate-limiting :scream:
        self.excludedLinks = open("monitor/reqs/excluded.txt", "r").read().splitlines()
        self.robloxLauncher = robloxLauncher
        self.timestamp = datetime.utcnow().replace(tzinfo=tzutc()).isoformat()
        self.monitorChannel()

    def monitorChannel(self):
        url = f"https://discord.com/api/v9/channels/{self.id}"
        response = requests.get(url, headers=self.headers)
        channelInfo = response.json()
        channelName = channelInfo.get('name')

        guildId = channelInfo.get('guild_id')
        guildInfo = requests.get(f"https://discord.com/api/v9/guilds/{guildId}", headers=self.headers).json()
        guildName = guildInfo.get('name')
        
        print(f"\n\033[38;5;208m[*]\033[0m Monitoring: {guildName} > {channelName} > {self.id}\n")

        while True:
            response = ChannelMonitor.session.get(self.url, headers=self.headers)
            if response.status_code == 200:
                for x in response.json():
                    msgTimestamp = parse(x["timestamp"])
                    if msgTimestamp < parse(self.timestamp):
                        continue

                    content = x["content"]
                    if "https://www.roblox.com/games/2788229376" in content and "privateServerLinkCode" in content:
                        regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
                        links = [link[0] for link in re.findall(regex, content)]

                        if len(links) == 1:
                            link = links[0]

                            if link not in self.excludedLinks:
                                self.robloxLauncher.startRoblox(link)
                                return
