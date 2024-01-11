import sqlite3

def create_database():
    conn = sqlite3.connect('films.db')
    cursor = conn.cursor()
    
    # Создаем таблицу films
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS films (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            film TEXT,
            user_id INTEGER,
            CONSTRAINT unique_film UNIQUE (film)
        )
    ''')
    
    conn.commit()
    conn.close()

# Вызываем функцию для создания базы данных
if __name__ == "__main__":
    create_database()