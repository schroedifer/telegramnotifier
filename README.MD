# TelegramNotifier

A Telegram bot to inform you of birthdays, holidays, events, etc.

## Background

Moving away from Facebook, I needed a better way to keep track of people's birthdays, anniversaries, holidays, or miscellaneous events.  I've tried using a calendar app, but the notifications just blended together with calendar notifications from my work calendar.  So, I wanted a way to notify myself of important things in a way I'd actually pay attention to.

You'll get a push notification:
* 14 days before
* 7 days before
* 1 days before
* The day of

## Prerequisites

* Python3
* Telegram account

## Setup Guide

### Create a virtual environment

        python3 -m venv venv

### Activate the virtual environment

Windows:

        source venv/Scripts/activate

Mac / Linux

        source venv/bin/activate

### Install the python modules

        pip install -r requirements.txt

### Create the Telegram Bot

I've used this guide to create a Telegram bot.  

1. Message `@BotFather` through the Telegram client
        
        `/start`

2. Create a bot

        `/newbot`

3. Name the bot

        `somebotname`

4. Give it a user name

        `somebotname_bot`

You'll be given the API key at this point.  The key, and the *_bot* name will be used in the *.env* file

* **Optional** give it a picture

### Get Your Telegram UserID

Message `@userinfobot`

Just starting a conversation with the bot will return your UserID

### Message your bot

Find your bot by searching for `@somebotname_bot` and hit 'message'.  You should see the following happen. 

        /start  

This lets the bot now start communicating with you.  

### Configure `.env`

The sample file *.env_sample* is provided to get you started.  Essentially:

```
TELEGRAM_TOKEN=<paste-token-here>
USER_ID=<paste-id-here>
```

Rename to *.env* and save.

### Configure 'dates.json'

The sample file *sample_dates.json* is provided to get you started.

The overall thought is that the dictionary is iterated through by the script, and each top-level key is another dictionary of dates associated with that key.  While not designed to be fully extensible, (ie, making custom categories) this shouldn't be too hard if a new category is desired.

Date format is `yyyy-mm-dd` or `mm-dd`.  Leading zeroes for months and days are ok.  

## Automating the job

I find it convenient to let the script run automatically on its own without my intervention.  I use a home server which I always keep on to run this program daily.  But a laptop or other device could be used as well, although a different configuration in the Chron or Windows Task Scheduler would be needed to run the script on power up or ensure it will run even if it missed the designated time.

### Linux / MacOS

### Configure the shell script

The provided shellscript `telegramnotifier.sh` will need to be updated with the correct paths.  The first argument is for the location for the python installation. 

A tool like [crontab guru](https://crontab.guru) is helpful for visualizing the crontab syntax

### Windows

As Crontab doesn't natively run on Windows, the Task Scheduler can be used.  The shell script isn't really needed here.  You can run the virtual environment python.exe and telegramnotifier.py script all at once.  

I've followed [this guide](https://www.askpython.com/python/examples/execute-python-windows-task-scheduler) to schedule python tasks.
* Create the task
    * The exectubale is `path/to/the/venv/Scripts/python.exe` for windows
    * The optional argument the path/to/the/telegramnotifier/telegramnotifier.py
