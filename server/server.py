import socket
import jsonpickle
import pyodbc

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 4000))
server.listen(1)
serverdb = 'localhost\\SQLEXPRESS'
database = 'calorie_diary_db'
conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={serverdb};DATABASE={database};Trusted_Connection=yes;'
db = pyodbc.connect(conn_str)
cursor = db.cursor()

def register_user(data):
    email = data['email']
    password = data['password']
    try:
        cursor.execute("INSERT INTO Users (email, password) VALUES (?, ?)", (email, password))
        db.commit()
        return 'registered'
    except:
        return 'email_taken'

def login_user(data):
    email = data['email']
    password = data['password']
    cursor.execute("SELECT * FROM Users WHERE email = ? AND password = ?", (email, password))
    if cursor.fetchone():
        cursor.execute("INSERT INTO logs_reg_aut (email, action_type) VALUES (?, 'login')", (email,))
        db.commit()
        return 'login_success'
    return 'login_failed'
def save_user_info(data):
    try:
        print(f"Сохраняем данные пользователя: {data}")
        cursor.execute("""
            INSERT INTO UserInfo (email, name, gender, birthdate, weight, height, goal)
            VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (data['email'], data['name'], data['gender'], data['birthdate'],
             data['weight'], data['height'], data['goal']))
        db.commit()
        return 'info_saved'
    except Exception as e:
        print(f"Ошибка при сохранении данных: {e}")
        return 'info_error'

while True:
    client, addr = server.accept()
    data = client.recv(1024).decode()
    obj = jsonpickle.decode(data)

    if obj['action'] == 'register':
        result = register_user(obj)
    elif obj['action'] == 'login':
        result = login_user(obj)
    elif obj['action'] == 'user_info':
        result = save_user_info(obj)
    else:
        result = 'unknown_action'

    client.send(result.encode())
    client.close()
