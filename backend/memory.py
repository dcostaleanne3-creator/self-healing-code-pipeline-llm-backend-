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

def get_progress_data():

    conn = sqlite3.connect("developer_memory.db")
    cursor = conn.cursor()

    # Error occurrences grouped by error_type
    cursor.execute("""
        SELECT error_type, COUNT(*)
        FROM errors
        GROUP BY error_type
    """)
    error_counts = dict(cursor.fetchall())

    # Quiz performance grouped by topic
    cursor.execute("""
        SELECT topic, COUNT(*), SUM(correct)
        FROM quiz_results
        GROUP BY topic
    """)
    quiz_rows = cursor.fetchall()

    # Overall summary numbers
    cursor.execute("SELECT COUNT(*) FROM errors")
    total_errors = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM fix_history")
    total_fixes = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*), SUM(correct) FROM quiz_results")
    total_attempts, total_correct = cursor.fetchone()
    total_attempts = total_attempts or 0
    total_correct = total_correct or 0

    conn.close()

    quiz_by_topic = {
        topic: {"attempts": attempts, "correct": correct or 0}
        for topic, attempts, correct in quiz_rows
    }

    return {
        "error_counts": error_counts,
        "quiz_by_topic": quiz_by_topic,
        "total_errors": total_errors,
        "total_fixes": total_fixes,
        "total_quiz_attempts": total_attempts,
        "total_quiz_correct": total_correct
    }