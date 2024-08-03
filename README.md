# An app that reminds you of things by making a thing pop up on the screen

## How to install:

- clone/download this repo
- cd to this directory.
- run the following commands:
  `chmod +x installer.bash`
  `./installer.bash`

- it will ask you for the sudo password, and you can just enter that to finish the installation.
- It needs sudo priviliges since it needs to install the reminder app as a startup process, and also needs to put the gui application in /usr/bin
- IMPORTANT: do not run the bash script itself as sudo, or it will install it in the wrong place and it won't work.

## How to use:

- after the installation, you should be able to type `reminder_app` and press enter in a terminal to start up the gui.
- here, you can add courses by entering the course name and slot (the slot must be a single capital letter).
- for the reminders, you can enter the message and the time, and it will remind you at that time with the message.
- the time must be in one of these formats:
  DD/MM/YYYY HH:MM
  or
  HH:MM
- if it's just HH:MM, it will remind you in the same day.
- if you want it to remind you at the same time every day, you can write the time in the HH:MM format, and the message must contain the word 'everyday' somewhere.
