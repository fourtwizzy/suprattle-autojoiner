from flask import Flask, render_template, request
import webbrowser
import time
import json
import logging
import requests
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


app = Flask(__name__)

run = False
delay = 3
joinedServers = []

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/start")
def start():
    global run
    global delay
    global joinedServers
    try:
        delay = int(request.args.get("delay"))
    except:
        try:
            delay = float(request.args.get("delay"))
        except:
            pass
    run = True
    print("Started")
    while run:
        try:
            url = "https://discordapp.com/api/v6/channels/"+request.args.get("channelId")+"/messages?limit=10"
            headers = {
            'authorization':request.args.get("accessToken")
            }
            r = requests.get(url,headers=headers)
            messageJson = json.loads(r.text)
            for message in messageJson:
                messageContent = message["content"]
                if "discord.gg" in messageContent or "discordapp.com/invite" in messageContent or "discord.com/invit" in messageContent:
                    inviteCode = (messageContent.split("discord")[1]).split("/")[1]
                    if "invite" in inviteCode:
                        inviteCode = inviteCode.split("/")[1]
                    inviteCode = (inviteCode.replace("/", "")).strip()
                    if inviteCode not in joinedServers:
                        data = {
                            "code": inviteCode,
                            "new_member": "true"
                        }
                        r = requests.post("https://discordapp.com/api/v6/invites/"+inviteCode,json=data,headers=headers)
                        print("Joined New Server - " + inviteCode)
                        joinedServers.append(inviteCode)
            time.sleep(delay)
        except:
            time.sleep(delay)
    return ""

@app.route("/stop")
def stop():
    global run
    run = False
    print("Stoped")
    return render_template("index.html")

if __name__ == "__main__":
    webbrowser.open_new_tab("http://127.0.0.1:5384")
    app.run('127.0.0.1', port=5384)
    app.run()
