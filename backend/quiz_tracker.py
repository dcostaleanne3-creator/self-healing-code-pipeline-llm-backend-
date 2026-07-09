import sqlite3


def analyze_quiz_performance():

    conn = sqlite3.connect("developer_memory.db")

    cursor = conn.cursor()

    cursor.execute("""
    SELECT topic,
           COUNT(*) as attempts,
           SUM(correct) as correct_answers
    FROM quiz_results
    GROUP BY topic
    """)

    results = cursor.fetchall()

    conn.close()

    print("\nQuiz Performance Report\n")

    for topic, attempts, correct_answers in results:

        accuracy = (
            correct_answers / attempts * 100
            if correct_answers is not None
            else 0
        )

        print(
            f"{topic}: "
            f"{accuracy:.1f}% accuracy "
            f"({correct_answers or 0}/{attempts})"
        )