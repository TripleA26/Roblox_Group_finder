import requests, random, threading, time, os, json, sys
from colorama import Fore
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
from discord_webhook import DiscordWebhook, DiscordEmbed
from dhooks import Webhook
from termcolor import cprint


software_names = [SoftwareName.CHROME.value]
operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
user_agent_rotator = UserAgent(
    software_names=software_names, operating_systems=operating_systems, limit=10000
)

proxyy = []
with open("config.json") as config:
    data = json.load(config)
    numb = data["timelapse"]
    wbh = data["Webhooks"]
    save = data["save"]
    prox = data["scrapper"]
    slfp = data['self_proxies']



hook = Webhook(wbh)
webhook = DiscordWebhook(wbh)


class stat:
    valid = 0
    Invalid = 0
    Locked = 0
    UnableToJoin = 0


def check():
    
    vl = False
    global proxyy
    agent = user_agent_rotator.get_random_user_agent()
    num = random.randint(1000000, 17500000)
    
    if prox == True and not slfp:
        if len(proxyy) <= 1:
            time.sleep(2)
            scrapper()
            proxy = "".join(random.choices(proxyy))
        else:
            proxy = "".join(random.choices(proxyy))
            
    if slfp == True:
        if len(proxyy) <= 1:
            print(f"[{Fore.LIGHTBLUE_EX}{time.strftime('%H:%M:%S')}{Fore.RESET}] {Fore.LIGHTYELLOW_EX}All the proxies has been ratelimited!{Fore.RESET}")
        proxy = random.choice(open('proxies.txt', 'r').read().splitlines())
        
    headers = {
        "authority"         : "groups.roblox.com",
        "accept"            : "application/json, text/plain, */*",
        "accept-language"   : "es,es-ES;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "origin"            : "https://www.roblox.com",
        "referer"           : "https://www.roblox.com/",
        "sec-ch-ua"         : '"Microsoft Edge";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        "user-agent"        : agent,
    }
    try:
        
        if prox == True or slfp == True:
            response = requests.get(
                f"https://groups.roblox.com/v1/groups/{num}",
                headers=headers,
                proxies={"http": f"http://{proxy}", "https": f"http://{proxy}"},
            )
            
        else:
            response = requests.get(
                f"https://groups.roblox.com/v1/groups/{num}", headers=headers
            )
            
        if "Too many requests" in response.text:
            print(
                f"[{Fore.LIGHTBLUE_EX}{time.strftime('%H:%M:%S')}{Fore.RESET}] {Fore.LIGHTYELLOW_EX}Proxy Limited:{Fore.RESET} {proxy}"
            )
            return
        
        try:
            owner = response.json()["owner"]["username"]
            print(
                f"[{Fore.LIGHTBLUE_EX}{time.strftime('%H:%M:%S')}{Fore.RESET}] {Fore.LIGHTRED_EX}Group with owner{Fore.RESET}  Id:{response.json()['id']}{Fore.RESET}"
            )
            stat.Invalid += 1
            
        except:
            
            if "Group is invalid or does not exist." in response.text:
                print(
                    f"[{Fore.LIGHTBLUE_EX}{time.strftime('%H:%M:%S')}{Fore.RESET}] {Fore.LIGHTRED_EX}Group invalid{Fore.RESET}     Id:{num}"
                )
                
                stat.Invalid += 1
                return
            
            if "isLocked" in response.text:
                if response.json()["isLocked"] == True:
                    print(
                        f"[{Fore.LIGHTBLUE_EX}{time.strftime('%H:%M:%S')}{Fore.RESET}] {Fore.LIGHTYELLOW_EX}Locked Group:{Fore.RESET}     Id:{response.json()['id']}"
                    )
                    stat.Locked += 1
                    return
                
            else:
                
                if response.json()["publicEntryAllowed"] == True:
                    
                    with open("Open_group.txt", "a+") as file:
                        
                        file.write(f"{response.json()['id']}\n")
                        print(
                            f"[{Fore.LIGHTBLUE_EX}{time.strftime('%H:%M:%S')}{Fore.RESET}] {Fore.LIGHTGREEN_EX}No owner found:{Fore.RESET} Id:{response.json()['id']}"
                        )
                        
                    webhook = DiscordWebhook(
                        wbh,
                        content=f"@everyone     `https://www.roblox.com/groups/{num}`",
                        username="Roblox Group Finder",
                        avatar_url="https://cdn.discordapp.com/guilds/930833528747347989/users/691236752404381719/avatars/3547235671123627fbeea56d70fe319c.png?size=4096",
                    )
                    
                    try:
                        
                        members = f"**{response.json()['memberCount']}**"
                        
                    except:
                        
                        members = "**Unable to Find The Member Count!**"
                    titl = f"**New Group**   Id: **{response.json()['id']}**"
                    desc = f"  Name: **{response.json()['name']}**   | Members: {members}"
                    embed = DiscordEmbed(
                        title=(titl), description=(desc), color="00008B"
                    )
                    webhook.add_embed(embed)
                    response = webhook.execute()
                    stat.valid += 1
                    return
                
                else:
                    if response.json()["publicEntryAllowed"] == False:
                        if save == True:
                            with open("Closed_group.txt", "a+") as file:
                                file.write(f"{response.json()['id']}\n")
                    print(
                        f"[{Fore.LIGHTBLUE_EX}{time.strftime('%H:%M:%S')}{Fore.RESET}] {Fore.LIGHTYELLOW_EX}No owner found:{Fore.RESET}   Id:{response.json()['id']}"
                    )
                    stat.UnableToJoin += 1

                    return
        vl = True
    except:
        pass
    try:
        if vl == False:
            proxyy.remove(proxy)
    except:
        pass


text = """ _______ _____  _____ _____  _      ______          
|__   __|  __ \|_   _|  __ \| |    |  ____|   /\    
   | |  | |__) | | | | |__) | |    | |__     /  \   
   | |  |  _  /  | | |  ___/| |    |  __|   / /\ \  
   | |  | | \ \ _| |_| |    | |____| |____ / ____ \ 
   |_|  |_|  \_\_____|_|    |______|______/_/    \_\ """

cprint(text, "magenta", attrs=["bold"], file=sys.stderr)
print("\n" * 2)
time.sleep(1.5)

if slfp == True and prox == True:
    print(f"[{Fore.LIGHTBLUE_EX}{time.strftime('%H:%M:%S')}{Fore.RESET}] {Fore.LIGHTRED_EX}Please disable scrapper or self proxies in config, the 2 cant be enable!{Fore.RESET}\n")
    time.sleep(3)
    exit()

def scrapper():
    global proxyy
    a = []
    url = "https://shorturl.at/gnzO1"
    r = requests.get(url)
    a.append(r.text)
    a = "".join(a)
    proxyy = a.split("\r\n")
    print(
        f"[{Fore.LIGHTBLUE_EX}{time.strftime('%H:%M:%S')}{Fore.RESET}] {Fore.LIGHTMAGENTA_EX}Scrapped {len(proxyy)} Proxies!{Fore.RESET}"
    )

if prox == True and not slfp:
    scrapper()
    
elif slfp == True and not prox:
    with open("proxies.txt") as f:
        amm = f.readlines()
        for line in amm:
            proxyy.append(line.strip())
        print(f"[{Fore.LIGHTBLUE_EX}{time.strftime('%H:%M:%S')}{Fore.RESET}] {Fore.LIGHTMAGENTA_EX}Imported {len(amm)} proxies from proxies.txt\n")
        
else:
  print(
    f"[{Fore.LIGHTBLUE_EX}{time.strftime('%H:%M:%S')}{Fore.RESET}] {Fore.LIGHTMAGENTA_EX}Running without proxies.\n{Fore.RESET}[{Fore.LIGHTBLUE_EX}{time.strftime('%H:%M:%S')}{Fore.RESET}] {Fore.LIGHTMAGENTA_EX}Remember that running without proxies, you will be rate limited so fast\n"
  )
  
       
time.sleep(2)
s = True
while True:
    for i in range(numb):
       if s == True:
        try:
            if i % (numb / 16) == 0:
                    os.system(
                        f"title TripleA Roblox Group Finder ^| Valid - {stat.valid} ^| Invalid - {stat.Invalid} ^| Locked - {stat.Locked} ^| Unable to Join - {stat.UnableToJoin}"
                    )
        except:
            s = False
            pass
        threading.Thread(target=check).start()
    if prox == True:
        scrapper()
