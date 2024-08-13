#!/usr/bin/python3
import tkinter as tk
import datetime
import time
import os
import playsound
import threading

try:
    import socket

    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    ## Create an abstract socket, by prefixing it with null.
    s.bind("\0postconnect_gateway_notify_lock")
except socket.error as e:
    error_code = e.args[0]
    error_string = e.args[1]
    print("Process already running. Exiting")
    exit(0)

# change these to the absolute path of the reminders and courses files
reminders_file = "reminders.txt"
courses_file = "courses.txt"
log_file = "reminder_app_logs.txt"

with open(log_file, "a") as file:
    file.write(str(datetime.datetime.now()))

slots = {
    "A": {0: "9:00", 2: "11:00", 3: "10:00"},
    "B": {0: "10:00", 2: "9:00", 3: "11:00"},
    "C": {0: "11:00", 2: "10:00", 3: "9:00"},
    "D": {0: "12:00", 1: "9:00", 4: "11:00"},
    "E": {1: "10:00", 3: "12:00", 4: "9:00"},
    "F": {1: "11:00", 2: "14:30", 4: "10:00"},
    "G": {1: "12:00", 2: "12:00", 4: "12:00"},
    "P": {0: "14:30", 3: "16:00"},
    "Q": {0: "16:00", 3: "14:30"},
    "R": {1: "14:30", 4: "16:00"},
    "S": {1: "16:00", 4: "14:30"},
}


def is_time_greater_eq(hour1, minute1, hour2, minute2, second1=0, second2=0):
    return (hour1 > hour2) or (
        (hour1 == hour2)
        and ((minute1 > minute2) or ((minute1 == minute2) and (second1 >= second2)))
    )


for k in slots.keys():
    for k2 in slots[k].keys():
        slots[k][k2] = [int(x) for x in slots[k][k2].split(":")]

# print(slots)
# root.withdraw()


def play_notification_sound():
    thread = threading.Thread(
        target=playsound.playsound,
        args=["reminder_sound.wav"],
    )
    thread.start()


def show_message(title, message, is_snoozable=False):
    play_notification_sound()
    global is_snoozed
    root = tk.Tk()
    # root = tk.Toplevel(root)
    root.title(title)
    # root.geometry("400x0")
    root.config(bg="black")

    root_label = tk.Label(
        root, text=message, fg="white", bg="#000000", font=("TkDefaultFont", 12)
    )
    root_label.pack(pady=30, padx=500)

    button_label = tk.Label(root)
    button_label.config(bg="black")

    ok = tk.Button(
        button_label, text="OK", command=lambda: root.destroy(), bd=5, width=13
    )
    ok2 = tk.Button(
        button_label,
        text="Shut up I know",
        command=lambda: root.destroy(),
        bd=5,
        width=13,
    )
    is_snoozed = False

    def snooze():
        global is_snoozed
        root.destroy()
        is_snoozed = True

    ok.grid(row=0, column=0, pady=20, padx=30)
    ok2.grid(row=0, column=1, pady=20, padx=30)
    if is_snoozable:
        ok3 = tk.Button(
            button_label,
            text="Snooze",
            command=lambda: snooze(),
            bd=5,
            width=13,
        )
        ok3.grid(row=0, column=2, pady=20, padx=30)
    button_label.pack()

    # makes the window borderless and puts it in the center. don't know/remember why wait_visibility is required
    root.overrideredirect(True)
    root.eval("tk::PlaceWindow . center")
    root.wait_visibility(root)

    # makes the popup slightly transluscent
    root.attributes("-alpha", 0.8)

    root.mainloop()

    return is_snoozed


if not (os.path.isfile(reminders_file) and os.path.isfile(courses_file)):
    show_message(
        "",
        'Bruh, You need to have reminders.txt and courses.txt files in the same directory as this code.\nIn reminders.txt, for each reminder, first there should be a line\nwhich has the date in one of these formats: "HH:MM" or "DD/MM/YY HH:MM".\nThen next line should be the message. If you want this to remind you every day,\nthe message should just contain the word "everyday" somewhere.\nFor the courses, Each course is one line, just write the course name, and the last letter\nof each line should just be the slot that the course is in (capital letter)\nYou can find these two files in ~/.config/reminder_app',
    )
    exit()

courses = []
reminders = []


# I don't even remember how the rest of this code got so messy, but I'm afraid to change anything because it will break it.
# It works fine, so I don't think there's a need to refactor it unless I need to add something

# print(type(datetime.now().time()))
after_10_min = datetime.datetime.now() + datetime.timedelta(minutes=10)
prev_hour = after_10_min.hour
prev_minute = after_10_min.minute
new_reminders = []

CurrentDate = datetime.datetime.now()
prev_curr_hour = CurrentDate.hour
prev_curr_minute = CurrentDate.minute
prev_curr_second = CurrentDate.second

# time.sleep(60 - prev_curr_second + 1)
while True:
    # time.sleep(60 - datetime.datetime.now().second + 1)
    time.sleep(1)

    with open(reminders_file, "r") as file:
        reminders = file.readlines()
        reminders = [line for line in reminders if line.strip()]
    courses.clear()
    with open(courses_file, "r") as file:
        c = file.readlines()
        for line in c:
            line = line.rstrip()
            slot = line[-1]
            name = line[0:-1]
            courses.append((name, slot))
    # print(datetime.datetime.now().second)
    # print(datetime.datetime.now().second)
    after_10_min = datetime.datetime.now() + datetime.timedelta(minutes=10)
    hour = after_10_min.hour
    minute = after_10_min.minute
    day = datetime.datetime.today().weekday()
    # print(day)

    CurrentDate = datetime.datetime.now()
    curr_hour = CurrentDate.hour
    curr_minute = CurrentDate.minute
    curr_second = CurrentDate.second
    snooze_added = False

    for course_name, slot in courses:
        if slot not in slots:
            continue
        if day in slots[slot]:
            slot_hour, slot_minute = slots[slot][day]
            # print(course_name, slot, hour, minute)
            if is_time_greater_eq(
                hour, minute, slot_hour, slot_minute
            ) and not is_time_greater_eq(
                prev_hour, prev_minute, slot_hour, slot_minute
            ):
                show_message(
                    "Reminder!!!", "You have " + course_name + " class in 10 min!"
                )

    for i in range(len(reminders) // 2):
        date_str = reminders[2 * i].rstrip()
        text_str = reminders[2 * i + 1].rstrip()
        reminder_date = None
        try:
            reminder_date = datetime.datetime.strptime(date_str, "%d/%m/%Y %H:%M")
        except:
            try:
                curr_date_str = str(CurrentDate.date())
                reminder_date = datetime.datetime.strptime(
                    curr_date_str + " " + date_str, "%Y-%m-%d %H:%M"
                )
            except:
                continue
            # print(reminder_date)
        is_everyday = "everyday" in text_str.lower()
        # print(CurrentDate, reminder_date)
        if (CurrentDate > reminder_date) and (
            not is_everyday
            or not is_time_greater_eq(
                prev_curr_hour,
                prev_curr_minute,
                reminder_date.hour,
                reminder_date.minute,
                prev_curr_second,
                reminder_date.second,
            )
        ):
            # print(
            #     prev_curr_hour,
            #     prev_curr_minute,
            #     reminder_date.hour,
            #     reminder_date.minute,
            # )
            if show_message("Reminder!!!", text_str, is_snoozable=True):
                snoozed_time = (
                    str(after_10_min.day)
                    + "/"
                    + str(after_10_min.month)
                    + "/"
                    + str(after_10_min.year)
                    + " "
                    + str(after_10_min.hour)
                    + ":"
                    + str(after_10_min.minute)
                )
                new_reminders.append(snoozed_time)
                new_reminders.append(text_str.replace("everyday", "snoozed"))
                snooze_added = True
                # print(snoozed_time, text_str.replace("everyday", "snoozed"))
            if is_everyday:
                new_reminders.append(date_str)
                new_reminders.append(text_str)
        else:
            new_reminders.append(date_str)
            new_reminders.append(text_str)

    if len(reminders) - len(new_reminders) >= 2 or snooze_added:
        with open(reminders_file, "w") as file:
            for line in new_reminders:
                file.write(line + "\n")
        reminders = new_reminders
    new_reminders = []

    prev_hour = hour
    prev_minute = minute
    prev_curr_hour = curr_hour
    prev_curr_minute = curr_minute
    prev_curr_second = curr_second
