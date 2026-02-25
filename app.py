import os
import sqlite3
from datetime import datetime
# Добавили send_from_directory
from flask import Flask, request, jsonify, redirect, send_from_directory
# Рекомендуется оставить CORS, даже если все с одного домена, на всякий случай
from flask_cors import CORS

# Определяем путь к папке сборки (она теперь рядом с app.py)
build_dir = 'build'
static_folder_path = os.path.join(build_dir, 'static')

# Создаем приложение Flask
# static_folder указывает, где лежат статические файлы (js, css)
# static_url_path='/static' - это URL, по которому они будут доступны (совпадает с путями в index.html)
# template_folder больше не нужен
app = Flask(__name__, static_folder=static_folder_path)
CORS(app)

# --- База данных (остается как есть) ---
def get_db_connection():
    conn = sqlite3.connect('devices.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS devices (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            model TEXT NOT NULL,
            charge TEXT NOT NULL,
            connection_time TEXT NOT NULL,
            disconnection_time TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# --- API Маршруты (остаются как есть) ---
@app.route('/save', methods=['POST'])
def save_data():
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    name = data.get('name')
    model = data.get('model')
    charge = data.get('charge')
    connection_time = data.get('connection_time')
    disconnection_time = data.get('disconnection_time')

    if not name or not model or not charge or not connection_time or not disconnection_time:
         return jsonify({'error': 'Missing required data'}), 400

    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('''
            INSERT INTO devices (name, model, charge, connection_time, disconnection_time)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, model, charge, connection_time, disconnection_time))
        conn.commit()
    except Exception as e:
         return jsonify({'error': str(e)}), 500
    finally:
         conn.close()

    return jsonify({'message': 'Data saved successfully'}), 201

@app.route('/get_data', methods=['GET'])
def get_data():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM devices')
    rows = c.fetchall()
    conn.close()
    devices = [dict(row) for row in rows] # Упрощенное преобразование в список словарей
    return jsonify(devices)


# --- Маршруты для отдачи React приложения ---

# Отдаем index.html для корневого пути
@app.route('/')
def serve_index():
    # Проверяем, существует ли файл
    index_path = os.path.join(build_dir, 'index.html')
    if not os.path.exists(index_path):
        return "Error: index.html not found in build directory!", 404
    # Отправляем файл из папки build
    return send_from_directory(build_dir, 'index.html')

# Catch-all маршрут для поддержки React Router и отдачи других статических файлов из build
# Важно: он должен быть ПОСЛЕ ваших API маршрутов (/save, /get_data)
@app.route('/<path:path>')
def serve_react_app(path):
    # Проверяем, существует ли запрошенный файл напрямую в папке build
    # (например, manifest.json, favicon.ico и т.д.)
    path_in_build = os.path.join(build_dir, path)
    if path != "" and os.path.exists(path_in_build):
        # Если файл существует, отдаем его
        return send_from_directory(build_dir, path)
    else:
        # Иначе (если файл не найден или путь пустой)
        # предполагаем, что это путь для React Router,
        # и отдаем главный index.html
        index_path = os.path.join(build_dir, 'index.html')
        if not os.path.exists(index_path):
             return "Error: index.html not found in build directory!", 404
        return send_from_directory(build_dir, 'index.html')


# Создаем таблицу при импорте (для gunicorn)
create_table()

# --- Запуск приложения ---
if __name__ == '__main__':
    # Проверка существования папки build перед запуском
    if not os.path.isdir(build_dir):
        print(f"Error: Build directory '{build_dir}' not found.")
        print("Please run 'npm run build' in your frontend directory and place the 'build' folder inside the 'backend' directory.")
    else:
        print(f"Serving React app from '{build_dir}' folder...")
        app.run(host='0.0.0.0', port=5000, debug=True)