from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
import sqlite3
from gevent import monkey
from gevent import Greenlet


app = Flask(__name__)
socketio = SocketIO(app)
monkey.patch_all()
def background_thread():
    while True:
        # Отправляем обновление каждые 5 секунд
        socketio.sleep(5)
        socketio.emit('update_data', namespace='/test')
@app.route('/')
def display_table():
    # Подключаемся к базе данных
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()

    # Выполняем SQL-запрос для выборки данных из таблицы
    cursor.execute('SELECT * FROM my_table')
    data = cursor.fetchall()

    # Закрываем соединение
    conn.close()

    # Передаем данные в HTML-шаблон и отображаем таблицу
    return render_template('table.html', data=data)
@app.route('/api', methods=['POST'])
def receive_data():
    try:
        # Подключаемся к базе данных
        conn = sqlite3.connect('my_database.db')
        cursor = conn.cursor()

        # Извлекаем данные из JSON-параметра запроса
        data = request.json
        received_data = data.get('data')

        cursor.execute('SELECT * FROM my_table WHERE id = ?', (received_data,))
        existing_data = cursor.fetchone()

        if existing_data:
            # Если запись существует, увеличиваем счетчик
            cursor.execute('UPDATE my_table SET counter = counter + 1 WHERE id = ?', (received_data,))
        else:
            # Если запись не существует, создаем новую
            cursor.execute('INSERT INTO my_table (id, counter) VALUES (?, 1)', (received_data,))


        # Сохраняем изменения и закрываем соединение
        conn.commit()
        conn.close()

        # Отправляем обновление по веб-сокету
        socketio.emit('update_data', namespace='/test')

        return jsonify({'message': 'Data received and processed successfully'}), 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return False
@socketio.on('connect', namespace='/test')
def handle_connect():
    Greenlet.spawn(background_thread)
if __name__ == '__main__':
    socketio.run(app, debug=True, use_reloader=False, allow_unsafe_werkzeug=True)