import sqlite3


def create_database():

    conn = sqlite3.connect("developer_memory.db")

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS errors(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        error_type TEXT,
        error_message TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_error(error_info):

    conn = sqlite3.connect("developer_memory.db")

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO errors(error_type, error_message)
        VALUES (?,?)
        """,
        (
            error_info["error_type"],
            error_info["message"]
        )
    )

    conn.commit()
    conn.close()