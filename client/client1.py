import socket
import jsonpickle
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

def send_to_server(data):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 4000))
    client.send(jsonpickle.encode(data).encode())
    response = client.recv(1024).decode()
    client.close()
    return response

def register():
    email = entry_email.get()
    password = entry_password.get()
    confirm = entry_confirm.get()

    if not email or not password or password != confirm:
        messagebox.showerror("Ошибка", "Данные некорректны")
        return

    data = {"action": "register", "email": email, "password": password}
    response = send_to_server(data)

    if response == 'registered':
        messagebox.showinfo("Успех", "Регистрация прошла успешно")
        show_user_info(email)
    elif response == 'email_taken':
        messagebox.showerror("Ошибка", "Почта уже используется")
    else:
        messagebox.showerror("Ошибка", "Неизвестная ошибка")

def login():
    email = entry_email_login.get()
    password = entry_password_login.get()

    if not email or not password:
        messagebox.showerror("Ошибка", "Заполните все поля")
        return

    data = {"action": "login", "email": email, "password": password}
    response = send_to_server(data)

    if response == 'login_success':
        messagebox.showinfo("Успех", "Вход выполнен")
        show_user_info(email)

        data = {"action": "get_user_info", "email": email}
        user_data_json = send_to_server(data)

        if user_data_json != 'no_data' and user_data_json != 'error':
            user_data = jsonpickle.decode(user_data_json)
            entry_name.delete(0, tk.END)
            entry_name.insert(0, user_data['name'])

            var_gender.set(user_data['gender'])

            entry_birth.delete(0, tk.END)
            entry_birth.insert(0, user_data['birthdate'])

            entry_weight.delete(0, tk.END)
            entry_weight.insert(0, user_data['weight'])

            entry_height.delete(0, tk.END)
            entry_height.insert(0, user_data['height'])

            var_goal.set(user_data['goal'])
    else:
        messagebox.showerror("Ошибка", "Неверная почта или пароль")
def load_user_info(email):
    data = {"action": "get_user_info", "email": email}
    response = send_to_server(data)
    user_data = jsonpickle.decode(response)

    if user_data:
        entry_name.delete(0, tk.END)
        entry_name.insert(0, user_data.get("name", ""))

        var_gender.set(user_data.get("gender", "Мужской"))

        entry_birth.delete(0, tk.END)
        entry_birth.insert(0, user_data.get("birthdate", ""))

        entry_weight.delete(0, tk.END)
        entry_weight.insert(0, str(user_data.get("weight", "")))

        entry_height.delete(0, tk.END)
        entry_height.insert(0, str(user_data.get("height", "")))

        var_goal.set(user_data.get("goal", "Поддержание"))
def show_register():
    login_frame.pack_forget()
    register_frame.pack()

def show_login():
    register_frame.pack_forget()
    login_frame.pack()

def show_user_info(email):
    login_frame.pack_forget()
    register_frame.pack_forget()
    user_info_frame.pack()

    user_email_label.config(text=f"Пользователь: {email}")

def submit_user_info():
    name = entry_name.get()
    gender = var_gender.get()
    birth_date = entry_birth.get()
    weight = entry_weight.get()
    height = entry_height.get()
    goal = var_goal.get()

    if not name or not gender or not birth_date or not weight or not height or not goal:
        messagebox.showerror("Ошибка", "Заполните все поля")
        return

    try:
        birth_date = datetime.strptime(birth_date, "%d.%m.%Y").date()
    except ValueError:
        messagebox.showerror("Ошибка", "Некорректный формат даты")
        return

    user_data = {
        "action": "user_info",
        "email": user_email_label.cget("text").split(": ")[1],
        "name": name,
        "gender": gender,
        "birthdate": str(birth_date),
        "weight": weight,
        "height": height,
        "goal": goal
    }

    response = send_to_server(user_data)

    if response == 'info_saved':
        messagebox.showinfo("Сохранено", "Информация сохранена")
        show_calorie_calc()
    else:
        messagebox.showerror("Ошибка", "Ошибка при сохранении информации")
def show_calorie_calc():
    user_info_frame.pack_forget()
    calories_frame.pack()

def calculate_calories():
    gender = var_gender.get()
    try:
        weight = float(entry_weight.get())
        height = float(entry_height.get())
        age = (datetime.now().date() - datetime.strptime(entry_birth.get(), "%d.%m.%Y").date()).days // 365
    except:
        messagebox.showerror("Ошибка", "Некорректные данные")
        return

    activity = var_activity.get()
    multiplier = {"Низкий": 1.2, "Средний": 1.55, "Высокий": 1.9}.get(activity, 1.2)

    if gender == "Мужской":
        bmr = 88.36 + 13.4 * weight + 4.8 * height - 5.7 * age
    else:
        bmr = 447.6 + 9.2 * weight + 3.1 * height - 4.3 * age

    result = round(bmr * multiplier)

    lbl_result.config(text=f"Ваша дневная норма: {result} ккал")

    data = {
        "action": "save_calorie_result",
        "email": user_email_label.cget("text").split(": ")[1],
        "calories": result
    }
    send_to_server(data)

root = tk.Tk()
root.title("Калорийный дневник")
root.geometry("500x500")

register_frame = tk.Frame(root)
tk.Label(register_frame, text="Регистрация").grid(row=0, column=0, columnspan=2)
tk.Label(register_frame, text="Почта").grid(row=1, column=0)
entry_email = tk.Entry(register_frame)
entry_email.grid(row=1, column=1)
tk.Label(register_frame, text="Пароль").grid(row=2, column=0)
entry_password = tk.Entry(register_frame, show="*")
entry_password.grid(row=2, column=1)
tk.Label(register_frame, text="Повторите пароль").grid(row=3, column=0)
entry_confirm = tk.Entry(register_frame, show="*")
entry_confirm.grid(row=3, column=1)
tk.Button(register_frame, text="Зарегистрироваться", command=register).grid(row=4, column=0, columnspan=2)
tk.Button(register_frame, text="У меня уже есть аккаунт", command=show_login).grid(row=5, column=0, columnspan=2)

login_frame = tk.Frame(root)
tk.Label(login_frame, text="Авторизация").grid(row=0, column=0, columnspan=2)
tk.Label(login_frame, text="Почта").grid(row=1, column=0)
entry_email_login = tk.Entry(login_frame)
entry_email_login.grid(row=1, column=1)
tk.Label(login_frame, text="Пароль").grid(row=2, column=0)
entry_password_login = tk.Entry(login_frame, show="*")
entry_password_login.grid(row=2, column=1)
tk.Button(login_frame, text="Войти", command=login).grid(row=3, column=0, columnspan=2)
tk.Button(login_frame, text="Зарегистрироваться", command=show_register).grid(row=4, column=0, columnspan=2)

user_info_frame = tk.Frame(root)
user_email_label = tk.Label(user_info_frame, text="Пользователь:")
user_email_label.grid(row=0, column=0, columnspan=2)

tk.Label(user_info_frame, text="Имя").grid(row=1, column=0)
entry_name = tk.Entry(user_info_frame)
entry_name.grid(row=1, column=1)

tk.Label(user_info_frame, text="Пол").grid(row=2, column=0)
var_gender = tk.StringVar()
tk.OptionMenu(user_info_frame, var_gender, "Мужской", "Женский").grid(row=2, column=1)

tk.Label(user_info_frame, text="Дата рождения").grid(row=3, column=0)
entry_birth = tk.Entry(user_info_frame)
entry_birth.grid(row=3, column=1)

tk.Label(user_info_frame, text="Вес (кг)").grid(row=4, column=0)
entry_weight = tk.Entry(user_info_frame)
entry_weight.grid(row=4, column=1)

tk.Label(user_info_frame, text="Рост (см)").grid(row=5, column=0)
entry_height = tk.Entry(user_info_frame)
entry_height.grid(row=5, column=1)

tk.Label(user_info_frame, text="Цель").grid(row=6, column=0)
var_goal = tk.StringVar()
tk.OptionMenu(user_info_frame, var_goal, "Похудение", "Поддержание", "Набор массы").grid(row=6, column=1)

tk.Button(user_info_frame, text="Сохранить", command=submit_user_info).grid(row=7, column=0, columnspan=2)
tk.Button(user_info_frame, text="Перейти к расчёту калорий", command=show_calorie_calc).grid(row=8, column=0, columnspan=2)

calories_frame = tk.Frame(root)
tk.Label(calories_frame, text="Выберите уровень активности").grid(row=0, column=0)
var_activity = tk.StringVar(value="Средний")
tk.OptionMenu(calories_frame, var_activity, "Низкий", "Средний", "Высокий").grid(row=0, column=1)

tk.Button(calories_frame, text="Рассчитать", command=calculate_calories).grid(row=1, column=0, columnspan=2)
lbl_result = tk.Label(calories_frame, text="")
lbl_result.grid(row=2, column=0, columnspan=2)
show_login()
root.mainloop()