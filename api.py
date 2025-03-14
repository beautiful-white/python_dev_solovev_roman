from fastapi import FastAPI, HTTPException
import sqlite3
import pandas as pd

app = FastAPI()

def connect_to_database(database_path):
    return sqlite3.connect(database_path)

def fetch_user_id(database_connection, user_login):
    query = f"SELECT id FROM author WHERE login = ?"
    result = pd.read_sql_query(query, database_connection, params=(user_login,))
    if result.empty:
        raise HTTPException(status_code=404, detail="User not found")
    return result.iloc[0, 0]

@app.get("/api/comments")
def fetch_user_comments(user_login: str):
    authors_db_connection = connect_to_database('authors_database.db')
    try:
        user_id = fetch_user_id(authors_db_connection, user_login)
        comments_query = f"""
        SELECT 
            a.login,
            p.header,
            a2.login as author_login,
            COUNT(c.id) as comment_count
        FROM comment c
        JOIN author a ON c.author_id = a.id
        JOIN post p ON c.post_id = p.id
        JOIN author a2 ON p.author_id = a2.id
        WHERE a.login = '{user_login}'
        GROUP BY p.header, a2.login
        """
        comments_data = pd.read_sql_query(comments_query, authors_db_connection)
        return comments_data.to_dict(orient="records")
    finally:
        authors_db_connection.close()

@app.get("/api/general")
def fetch_user_activity(user_login: str):
    authors_db_connection = connect_to_database('authors_database.db')
    logs_db_connection = connect_to_database('logs_database.db')
    try:
        user_id = fetch_user_id(authors_db_connection, user_login)
        activity_query = f"""
        SELECT 
            DATE(l.datetime) as date,
            SUM(l.event_type_id = (SELECT id FROM event_type WHERE name = 'login')) as login_count,
            SUM(l.event_type_id = (SELECT id FROM event_type WHERE name = 'logout')) as logout_count,
            SUM(l.space_type_id = (SELECT id FROM space_type WHERE name = 'blog')) as blog_actions_count
        FROM logs l
        WHERE l.user_id = {user_id}
        GROUP BY DATE(l.datetime)
        """
        activity_data = pd.read_sql_query(activity_query, logs_db_connection)
        return activity_data.to_dict(orient="records")
    finally:
        authors_db_connection.close()
        logs_db_connection.close()