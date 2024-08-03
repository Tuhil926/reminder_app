#!/bin/bash

if [ "$EUID" -eq 0 ]
  then echo "Please don't run as root"
  exit
fi

mkdir ~/.config/reminder_app
cp reminder_app.py ~/.config/reminder_app
chmod +x ~/.config/reminder_app/reminder_app.py
cp reminder_app_settings.py ~/.config/reminder_app
chmod +x ~/.config/reminder_app/reminder_app_settings.py
cp reminder_sound.wav ~/.config/reminder_app
cp reminder_app_logs.txt ~/.config/reminder_app
cp reminders.txt ~/.config/reminder_app
cp courses.txt ~/.config/reminder_app
chmod +x reminder_app_startup.sh
sudo cp reminder_app_startup.sh /etc/profile.d
chmod +x reminder_app
sudo cp reminder_app /usr/bin

pip install playsound

./reminder_app_startup.sh
echo Installed! You run the command "reminder_app" to configure your courses and reminders