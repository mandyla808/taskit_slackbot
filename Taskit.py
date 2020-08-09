import threading
import requests
import json
import config
from slack.web.client import WebClient
from slack.errors import SlackApiError

class toDoList(object):
    def __init__(self):
        self.Tasks = set([])
        self.Done = set([])

    def AddTask(self, newTask):
        if newTask in self.Tasks:
            return "It's already on your list!"
        self.Tasks.add(newTask)
        return "New task added. Get to work!"

    def FinishTask(self, oldTask):
        if not (oldTask in self.Tasks):
            return "It's not on your list..."
        self.DeleteTask(oldTask)
        self.Done.add(oldTask)
        return "Finished another one? Nice!"

    def DeleteTask(self, oldTask):
        if not (oldTask in self.Tasks):
            return "It's not on your list..."
        self.Tasks.remove(oldTask)
        return "We took it off your list. Whew!"

    def Clean(self):
        self.Done = set([])

    def ViewTasks(self):
        numTasks = len(self.Tasks)
        numDone = len(self.Done)
        if numTasks + numDone == 0:
            return "No tasks... yet"
        res = ""
        if numTasks != 0:
            res += ":white_medium_square: "
            i = 0
            for task in self.Tasks:
                res += task
                if i != numTasks - 1:
                    res += "\n:white_medium_square: "
                i += 1
            if numDone != 0:
                res += "\n"
        if numDone != 0:
            res += ":heavy_check_mark: ~"
            i = 0
            for task in self.Done:
                res += task
                if i != numDone - 1:
                    res += "~\n:heavy_check_mark: ~"
                i += 1
            res += "~"
        return res

    def Publicize(self, channel, task, user):
        if task in self.Done:
            msg = "WooHoo!:tada: <@" + user + "> just completed a task!\n:heavy_check_mark: " + task
            sendMessage(channel, msg)
            return "It's public!"
        elif task in self.Tasks:
            msg = "Wowwie!:clap::clap::clap: <@" + user + "> just started a task!\n :white_medium_square: " + task
            sendMessage(channel, msg)
            return "It's public!"
        else:
            return "That task is not on your list. Add it before you publicize it!"

    def HelpCommand(self):
        return "Usage: /taskit add <task> || /taskit finish <task> || /taskit remove <task> || /taskit view || /taskit clean"


def Handler(toDos, user, message):
    message = message.split(' ')
    command = message[0]
    message = message[1:]
    notFound = "Invalid input"
    if command == "help":
        return toDos.HelpCommand()
    elif command == "add":
        if len(message) == 0:
            return notFound
        else:
            return toDos.AddTask(' '.join(message))
    elif command == "finish":
        if len(message) == 0:
            return notFound
        else:
            return toDos.FinishTask(' '.join(message))
    elif command == "remove":
        if len(message) == 0:
            return notFound
        else:
            return toDos.DeleteTask(' '.join(message))
    elif command == "view":
        return toDos.ViewTasks()
    elif command == "clean":
        return toDos.Clean()
    elif command == "publicize":
        if len(message) == 0:
            return notFound
        else:
            return toDos.Publicize(message[0], (' '.join(message[1:])), user)
    else:
        return "Your command could not be found or was malformed, please type (/taskit help) for more details"


def sendMessage(tryChannel, msg):
    slack_client = WebClient(config.SLACK_BOT_TOKEN)
    try:
        slack_client.chat_postMessage(
        channel = tryChannel,
        text = msg
        )
    except SlackApiError as e:
        if e.response["error"] == "channel_not_found":
            return "We can't find this channel:confused:"
        elif e.response["error"] == "not_in_channel":
            return "Taskit is not in this channel. Please invite us:grin:"
        else:
            return "Sorry something went wrong:confused:"


def PostMessage(message):
    webhook_url = config.webhook_url
    slack_data = {'text': message, 'response_type': 'in_channel'}
    response = requests.post(webhook_url, data=json.dumps(slack_data), headers={'Content-Type': 'application/json'})
