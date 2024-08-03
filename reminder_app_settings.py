#!/usr/bin/python3
import tkinter as tk
import threading
import time as tm

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

root = tk.Tk()
root.title("Reminder App")
# root.geometry("800x500")
root.config(bg="black")

reminders_file = "reminders.txt"
courses_file = "courses.txt"
courses = []
reminders = []


def retrieve_files():
    global reminders, courses
    with open(reminders_file, "r") as file:
        reminders = file.readlines()
        reminders = [line.strip() for line in reminders if line.strip()]
    courses = []
    with open(courses_file, "r") as file:
        c = file.readlines()
        for line in c:
            line = line.rstrip()
            slot = line[-1]
            name = line[0:-1].rstrip()
            courses.append((name, slot))


def save_reminders():
    with open(reminders_file, "w") as file:
        for line in reminders:
            file.write(line + "\n")


def save_courses():
    with open(courses_file, "w") as file:
        for name, slot in courses:
            file.write(name + " " + slot + "\n")


retrieve_files()

running = True

courses_and_reminders = tk.Label(root, bg="black")
reminders_elem = tk.Label(courses_and_reminders, bg="black", fg="white")
reminder_list = tk.Listbox(
    reminders_elem, selectmode=tk.SINGLE, width=90, bg="black", fg="white", border=5
)


def periodic_retriever():
    global reminders
    while running:
        tm.sleep(1)
        with open(reminders_file, "r") as file:
            new_reminders = file.readlines()
            new_reminders = [line.strip() for line in new_reminders if line.strip()]
            diff = False
            for i in range(min(len(new_reminders), len(reminders))):
                if reminders[i] != new_reminders[i]:
                    diff = True
                    break
            if len(reminders) != len(new_reminders) or diff:
                for i in range(len(reminders) // 2):
                    reminder_list.delete(0)
                reminders = new_reminders
                for i in range(len(reminders) // 2):
                    reminder_list.insert(
                        i, "(" + reminders[i * 2] + ")" + " " + reminders[i * 2 + 1]
                    )


retriever_thread = threading.Thread(target=periodic_retriever)
retriever_thread.start()

course_elems = []
reminder_elems = []
time_table = tk.Label(root, bg="#181818")


def remove_course(i, course_list):
    global time_table
    del courses[i]
    course_list.delete(i)
    save_courses()
    render_days(time_table)


def add_course(name, slot, course_list):
    global time_table
    course_list.insert(
        len(courses), name.get(1.0, "end-1c") + " " + slot.get(1.0, "end-1c")
    )
    # print(name.get(1.0, "end-1c") + " " + slot.get(1.0, "end-1c"))
    courses.append((name.get(1.0, "end-1c"), slot.get(1.0, "end-1c")))
    name.delete(1.0, tk.END)
    slot.delete(1.0, tk.END)
    save_courses()
    render_days(time_table)


def remove_reminder(i, reminder_list):
    del reminders[i * 2 + 1]
    del reminders[i * 2]
    reminder_list.delete(i)
    save_reminders()


def add_reminder(msg, time, reminder_list):
    reminder_list.insert(
        len(reminders),
        "(" + time.get(1.0, "end-1c") + ")" + " " + msg.get(1.0, "end-1c"),
    )
    reminders.append(time.get(1.0, "end-1c"))
    reminders.append(msg.get(1.0, "end-1c"))
    msg.delete(1.0, tk.END)
    time.delete(1.0, tk.END)
    save_reminders()


def list_index_courses(item):
    index = -1
    for i in range(len(courses)):
        if courses[i] == item:
            index = i
    return index


days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]


def render_days(parent):
    for item in parent.winfo_children():
        item.destroy()
    for day in range(5):
        # schedule[day].clear()
        wrapper = tk.Frame(parent, bg="#181818")
        wrapper.grid(row=0, column=day, padx=20, pady=20, sticky="n")
        weekday = tk.Label(wrapper, text=days[day], bg="#181818", fg="white")
        weekday.pack()
        for i in range(len(courses)):
            if courses[i][1] not in slots:
                continue
            if day in slots[courses[i][1]]:
                # schedule[day].append(
                #     courses[i][0] + "  -  " + slots[courses[i][1]][day]
                # )
                cours = tk.Label(
                    wrapper,
                    text=courses[i][0] + "  -  " + slots[courses[i][1]][day],
                    bg="#181818",
                    fg="white",
                )
                cours.pack(pady=10)


def render():
    global reminder_list, reminders_elem, courses_and_reminders
    i = 0
    courses_elem = tk.Label(courses_and_reminders, bg="black")
    txt1 = tk.Label(courses_elem, text="Courses registered", bg="black", fg="white")
    txt1.grid(row=0, column=0)
    course_list = tk.Listbox(
        courses_elem, selectmode=tk.SINGLE, width=40, bg="black", fg="white", border=5
    )
    for course_name, slot in courses:
        course_list.insert(i, course_name + " " + slot)
        i += 1
    remove_add = tk.Label(courses_elem, bg="black", fg="white")
    input_fields = tk.Label(courses_elem, bg="black", fg="white")
    name_label = tk.Label(input_fields, text="course:", bg="black", fg="white")
    name_label.grid(row=0, column=0)
    slot_label = tk.Label(input_fields, text="slot:", bg="black", fg="white")
    slot_label.grid(row=0, column=2)
    name = tk.Text(
        input_fields,
        width=20,
        height=1,
        bg="black",
        fg="white",
        border=5,
    )
    name.grid(row=0, column=1, pady=10, padx=10)
    slot = tk.Text(input_fields, width=5, height=1, bg="black", fg="white", border=5)
    slot.grid(row=0, column=3, pady=10, padx=10)

    add = tk.Button(
        remove_add,
        text="add",
        width=5,
        command=lambda: add_course(name, slot, course_list),
        bg="black",
        fg="white",
        border=5,
    )
    add.grid(row=1, column=0, pady=10, padx=10)
    remove = tk.Button(
        remove_add,
        text="remove",
        width=5,
        command=lambda: remove_course(course_list.index(tk.ACTIVE), course_list),
        bg="black",
        fg="white",
        border=5,
    )
    remove.grid(row=1, column=1, pady=10, padx=10)
    course_list.grid(row=1, column=0)
    remove_add.grid(row=3, column=0)
    input_fields.grid(column=0, row=2)
    courses_elem.grid(row=0, column=0, padx=10)

    # reminders
    i = 0

    txt1 = tk.Label(reminders_elem, text="Reminders", bg="black", fg="white")
    txt1.grid(row=0, column=0)
    # print(reminders)
    for i in range(len(reminders) // 2):
        reminder_list.insert(
            i, "(" + reminders[i * 2] + ")" + " " + reminders[i * 2 + 1]
        )
    input_fields2 = tk.Label(reminders_elem, bg="black", fg="white")
    remove_add2 = tk.Label(reminders_elem, bg="black", fg="white")
    msg_label = tk.Label(input_fields2, text="message", bg="black", fg="white")
    msg_label.grid(row=0, column=0)
    time_of_msg_label = tk.Label(input_fields2, text="time", bg="black", fg="white")
    time_of_msg_label.grid(row=0, column=2)
    msg = tk.Text(input_fields2, width=50, height=1, bg="black", fg="white", border=5)
    msg.grid(row=0, column=1, pady=10, padx=10)
    time_of_msg = tk.Text(
        input_fields2, width=20, height=1, bg="black", fg="white", border=5
    )
    time_of_msg.grid(row=0, column=3, pady=10, padx=10)

    add2 = tk.Button(
        remove_add2,
        text="add",
        width=5,
        command=lambda: add_reminder(msg, time_of_msg, reminder_list),
        bg="black",
        fg="white",
        border=5,
    )
    add2.grid(row=1, column=0, pady=10, padx=10)
    remove2 = tk.Button(
        remove_add2,
        text="remove",
        width=5,
        command=lambda: remove_reminder(reminder_list.index(tk.ACTIVE), reminder_list),
        bg="black",
        fg="white",
        border=5,
    )
    remove2.grid(row=1, column=1, pady=10, padx=10)
    reminder_list.grid(row=1, column=0)
    remove_add2.grid(row=3, column=0)
    input_fields2.grid(row=2, column=0)
    reminders_elem.grid(row=0, column=1, padx=10)
    courses_and_reminders.grid(row=0, column=0)

    # Time table
    render_days(time_table)
    time_table.grid(row=1, column=0, pady=20)


render()


root.mainloop()
running = False
retriever_thread.join()
