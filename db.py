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

#алгоритм поиска схожего названия если не хватит UNIQUE
"""
def insert_film(film, user_id):
    cursor.execute('''
                   SELECT COUNT(*) FROM films WHERE film = ? AND user_id = ?
                   ''', (film, user_id))
    count = cursor.fetchone()[0]
    if count == 0:
        cursor.execute('''
                       INSERT INTO films (film, user_id) VALUES (?, ?)
                       ''', (film, user_id))
        conn.commit()
        print("Фильм " + film + " добавлен")
    else:
        print("Фильм " + film + " уже был добавлен ранее")

conn.close()
"""