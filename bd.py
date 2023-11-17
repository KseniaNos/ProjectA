import sqlite3

# Создаем соединение с базой данных (если базы данных нет, она будет создана)
conn = sqlite3.connect('my_database.db')

# Создаем объект-курсор для выполнения SQL-запросов
cursor = conn.cursor()

# Создаем таблицу с двумя столбцами: id (INTEGER) и counter (INTEGER)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS my_table (
        id INTEGER PRIMARY KEY,
        counter INTEGER
    )
''')

# Сохраняем изменения и закрываем соединение
conn.commit()
conn.close()