import socket
import jsonpickle
import tkinter as tk
from tkinter import messagebox

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
        show_login()
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
        root.destroy()
    else:
        messagebox.showerror("Ошибка", "Неверная почта или пароль")

def show_register():
    login_frame.pack_forget()
    register_frame.pack()

def show_login():
    register_frame.pack_forget()
    login_frame.pack()

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

show_login()

root.mainloop()
