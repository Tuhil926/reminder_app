#!/bin/bash

cd ~/.config/reminder_app
# the & here is essential, or the os will deadlock as soon as you log in. Guess how I found that out
./reminder_app.py > reminder_app_logs.txt &