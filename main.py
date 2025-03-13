import sqlite3
import pandas as pd

# Функция для подключения к базе данных
def connect_to_db(db_path):
    return sqlite3.connect(db_path)

# Функция для формирования датасета comments
def get_comments_dataset(db1_conn, db2_conn, user_login):
    # Запрос для получения данных о комментариях
    query = """
    SELECT 
        a.login AS user_login,
        p.header AS post_header,
        author.login AS post_author_login,
        COUNT(l.id) AS comment_count
    FROM logs l
    JOIN db1.author a ON l.user_id = a.id
    JOIN db1.post p ON l.space_type_id = (SELECT id FROM space_type WHERE name = 'post')
    JOIN db1.author author ON p.author_id = author.id
    WHERE l.event_type_id = (SELECT id FROM event_type WHERE name = 'comment')
      AND a.login = ?
    GROUP BY p.header, author.login
    """
    # Выполнение запроса
    comments_df = pd.read_sql_query(query, db2_conn, params=(user_login,))
    return comments_df

# Функция для формирования датасета general
def get_general_dataset(db2_conn, user_login):
    # Запрос для получения общей информации о действиях пользователя
    query = """
    SELECT 
        DATE(datetime) AS date,
        SUM(CASE WHEN event_type_id = (SELECT id FROM event_type WHERE name = 'login') THEN 1 ELSE 0 END) AS login_count,
        SUM(CASE WHEN event_type_id = (SELECT id FROM event_type WHERE name = 'logout') THEN 1 ELSE 0 END) AS logout_count,
        SUM(CASE WHEN space_type_id = (SELECT id FROM space_type WHERE name = 'blog') THEN 1 ELSE 0 END) AS blog_actions_count
    FROM logs l
    JOIN db1.author a ON l.user_id = a.id
    WHERE a.login = ?
    GROUP BY DATE(datetime)
    """
    # Выполнение запроса
    general_df = pd.read_sql_query(query, db2_conn, params=(user_login,))
    return general_df

# Основная функция
def main():
    # Пути к базам данных
    db1_path = 'authors_database.db'
    db2_path = 'logs_database.db'

    # Подключение к базам данных
    db1_conn = connect_to_db(db1_path)
    db2_conn = connect_to_db(db2_path)

    # Логин пользователя для анализа
    user_login = 'user_login_example'  # Замените на нужный логин

    # Формирование датасетов
    comments_df = get_comments_dataset(db1_conn, db2_conn, user_login)
    general_df = get_general_dataset(db2_conn, user_login)

    # Вывод результатов
    print("Комментарии пользователя:")
    print(comments_df)
    print("\nОбщая информация о действиях пользователя:")
    print(general_df)

    # Закрытие соединений
    db1_conn.close()
    db2_conn.close()

if __name__ == "__main__":
    main()