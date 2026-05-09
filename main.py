import tkinter as tk
from tkinter import messagebox
import json
import random
import os

bd_name = "book.json"

#Работа с JSON

def load_tasks():
    if os.path.exists(bd_name):
        try:
            with open(bd_name, "r", encoding="utf-8") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return []
    return []



def save_tasks():
    with open(bd_name, "w", encoding="utf-8") as file:
        json.dump(history, file, ensure_ascii=False, indent=4)

#Предопределённые задачи

tasks = {
    "Учёба": [
        "Сделать уроки",
        "Повторить Python",
        "Потренироваться в написании кода"
    ],
    "Спорт": [
        "Сделать растяжку",
        "Пробежать 2 км",
        "Сделать базовую тренировку"
    ],
    "Работа": [
        "Проверить почту",
        "Подготовить отчёт",
        "Выполнить работу"
    ]
}

#История

history = load_tasks()

#Функции

def update_listbox(filtered_tasks=None):
    listbox_history.delete(0, tk.END)

    if filtered_tasks is None:
        filtered_tasks = history

    for item in filtered_tasks:listbox_history.insert(tk.END,f"[{item['category']}] {item['task']}")

def generate_task():
    category = category_var.get()

    if category == "Все":
        all_tasks = []
        for cat, task_list in tasks.items():
            for task in task_list:
                all_tasks.append((cat, task))

        selected_category, selected_task = random.choice(all_tasks)
    else:
        selected_task = random.choice(tasks[category])
        selected_category = category

    result_label.config(text=f"Задача: {selected_task}\nКатегория: {selected_category}")

    history.append({"category": selected_category,"task": selected_task})

    update_listbox()
    save_tasks()

def add_task():
    new_task = entry_task.get().strip()
    category = add_category_var.get()

    if not new_task:
        messagebox.showwarning("Ошибка","Введите текст задачи")
        return

    tasks[category].append(new_task)

    messagebox.showinfo("Вы добавили задачу","Новая задача добавлена")

    entry_task.delete(0, tk.END)

def filter_tasks():
    selected_category = category_var.get()

    if selected_category == "Все":
        update_listbox()
    else:
        filtered = [item for item in history if item["category"] == selected_category]
        update_listbox(filtered)

#GUI

root = tk.Tk()
root.title("Random Task Generator")
root.geometry("600x500")
root.configure(bg="#f0f0f0")


#Заголовок

label_title = tk.Label(root,text="Random Task Generator",font=("Arial", 18, "bold"),bg="#f0f0f0")
label_title.pack(pady=10)

#Фильтр

category_var = tk.StringVar(value="Все")

filter_frame = tk.Frame(root, bg="#f0f0f0")
filter_frame.pack(pady=5)

label_filter = tk.Label(filter_frame,text="Фильтр:",bg="#f0f0f0")
label_filter.pack(side=tk.LEFT, padx=5)

option_menu = tk.OptionMenu(filter_frame,category_var,"Все","Учёба","Спорт","Работа")
option_menu.pack(side=tk.LEFT)

btn_filter = tk.Button(filter_frame,text="Применить",command=filter_tasks)
btn_filter.pack(side=tk.LEFT, padx=5)

#Генерация задачи

btn_generate = tk.Button(root,text="Сгенерировать задачу",command=generate_task,bg="#4CAF50",fg="white",font=("Arial", 12))
btn_generate.pack(pady=10)

#Результат

result_label = tk.Label(root,text="Нажмите кнопку для генерации задачи",font=("Arial", 12),bg="#f0f0f0")
result_label.pack(pady=10)

#Добавление новой задачи

add_frame = tk.Frame(root, bg="#f0f0f0")
add_frame.pack(pady=10)

entry_task = tk.Entry(add_frame, width=30)
entry_task.pack(side=tk.LEFT, padx=5)

add_category_var = tk.StringVar(value="Учёба")

add_menu = tk.OptionMenu(add_frame,add_category_var,"Учёба","Спорт","Работа")
add_menu.pack(side=tk.LEFT)

btn_add = tk.Button(add_frame,text="Добавить задачу",command=add_task)
btn_add.pack(side=tk.LEFT, padx=5)

#История

label_history = tk.Label(root,text="История задач:",font=("Arial", 12, "bold"),bg="#f0f0f0")
label_history.pack(pady=5)

listbox_history = tk.Listbox(root, width=60, height=12)
listbox_history.pack(pady=10)

#Запуск

update_listbox()
root.mainloop()