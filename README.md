Task-It
======================

A Slack integration to keep track of tasks and allow users to publicize tasks
to channels. A to-do list within your Slack workspace helps keep you organized.
The option to publicize tasks provides motivation and gives your co-workers
a better sense of what others are doing and what's happening in the organization
in general.

Usage (from within Slack, presumes set up with /taskit as the slash cmd):

<code> /taskit add <task> </code> Adds <task> to your list

<code> /taskit finish <task> </code> Cross <task> off your list

<code> /taskit remove <task> </code> Remove <task> without completing it

<code> /taskit view </code> View your task list

<code> /taskit clean </code> Clean up your list by removing all finished tasks

This app requires deployment. To do this for free, you can use Heroku. To try
this app locally you can use ngrok.

1) Go to https://api.slack.com/apps?new_app=1 to create an app for your workspace.

2) Click "Slash Commands" and add a command called "/taskit" with the request
URL given by your deployment service followed by /slack/test

3) Go to the Incoming Webhook tab, and add a webhook. This will be your webhook_url.

4) Co to the OAuth & Permissions tab. Copy the Bot User OAuth Access Token. This
is your SLACK_BOT_TOKEN.

5) Clone this repo, and paste the webhook_url and SLACK_BOT_TOKEN in config.py.

6) Run app.py and your ready to go!
