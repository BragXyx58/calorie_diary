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
def get_user_info(email):
    try:
        cursor.execute("SELECT name, gender, birthdate, weight, height, goal FROM UserInfo WHERE email = ?", (email,))
        row = cursor.fetchone()
        if row:
            return jsonpickle.encode({
                "name": row[0],
                "gender": row[1],
                "birthdate": row[2].strftime("%d.%m.%Y"),
                "weight": row[3],
                "height": row[4],
                "goal": row[5]
            })
        else:
            return 'no_data'
    except Exception as e:
        print(f"Ошибка при получении данных пользователя: {e}")
        return 'error'
def save_calorie_result(data):
    try:
        cursor.execute("INSERT INTO CalorieHistory (email, calories) VALUES (?, ?)",
                       (data['email'], data['calories']))
        db.commit()
        return 'calories_saved'
    except Exception as e:
        print(f"Ошибка при сохранении калорий: {e}")
        return 'calorie_error'
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
    elif obj['action'] == 'save_calorie_result':
        result = save_calorie_result(obj)
    elif obj['action'] == 'get_user_info':
        result = get_user_info(obj['email'])
    else:
        result = 'unknown_action'

    client.send(result.encode())
    client.close()
