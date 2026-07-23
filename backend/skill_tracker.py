import sqlite3


topic_map = {
    "TypeError": "Python data types and type conversion",
    "IndexError": "List indexing and bounds checking",
    "NameError": "Variables and scope",
    "SyntaxError": "Python syntax and indentation",
    "TimeoutError": "Infinite loops and program logic",
    "ZeroDivisionError": "Arithmetic and division safety",
    "KeyError": "Dictionary keys and lookups",
    "AttributeError": "Object attributes and methods",
    "ValueError": "Data validation and type conversion",
    "IndentationError": "Python indentation rules"
}


def analyze_skill_gaps():

    conn = sqlite3.connect("developer_memory.db")

    cursor = conn.cursor()

    cursor.execute("""
    SELECT error_type, COUNT(*)
    FROM errors
    GROUP BY error_type
    ORDER BY COUNT(*) DESC
    """)

    results = cursor.fetchall()

    conn.close()

    print("\nDeveloper Learning Report\n")

    for error_type, count in results:

        print(f"{error_type}: {count} occurrence(s)")

        if error_type in topic_map:
            print(f"Recommended Topic: {topic_map[error_type]}")

        print()