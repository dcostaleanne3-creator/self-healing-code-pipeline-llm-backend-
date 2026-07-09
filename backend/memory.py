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

    cursor.execute("""
CREATE TABLE IF NOT EXISTS quiz_results(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic TEXT,
    correct INTEGER
)
""")
    
    cursor.execute("""
CREATE TABLE IF NOT EXISTS fix_history(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    error_type TEXT,
    original_code TEXT,
    fixed_code TEXT
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

def save_quiz_result(topic, correct):

    conn = sqlite3.connect("developer_memory.db")

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO quiz_results(topic, correct)
        VALUES (?, ?)
        """,
        (topic, correct)
    )

    conn.commit()
    conn.close()    

def save_fix_history(
    error_type,
    original_code,
    fixed_code
):

    conn = sqlite3.connect(
        "developer_memory.db"
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO fix_history(
            error_type,
            original_code,
            fixed_code
        )
        VALUES (?, ?, ?)
        """,
        (
            error_type,
            original_code,
            fixed_code
        )
    )

    conn.commit()
    conn.close()    

def get_error_count(error_type):

    conn = sqlite3.connect(
        "developer_memory.db"
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM errors
        WHERE error_type = ?
        """,
        (error_type,)
    )

    count = cursor.fetchone()[0]

    conn.close()

    return count    

def get_previous_fix(error_type):

    conn = sqlite3.connect(
        "developer_memory.db"
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT fixed_code
        FROM fix_history
        WHERE error_type = ?
        ORDER BY id DESC
        LIMIT 1
        """,
        (error_type,)
    )

    result = cursor.fetchone()

    conn.close()

    if result:
        return result[0]

    return None