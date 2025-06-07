import sqlite3
from datetime import datetime


def create_connection():
    """ایجاد ارتباط با پایگاه داده"""
    conn = None
    try:
        conn = sqlite3.connect('todo.db')
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn


def setup_database(conn):
    """تنظیم جداول پایگاه داده"""
    try:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            priority INTEGER DEFAULT 3,
            created_at TIMESTAMP,
            completed BOOLEAN DEFAULT 0
        )
        """)
        conn.commit()
    except sqlite3.Error as e:
        print(e)


def add_task(conn, title, priority=3):
    """افزودن وظیفه جدید"""
    try:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO tasks (title, priority, created_at)
        VALUES (?, ?, ?)
        """, (title, priority, datetime.now()))
        conn.commit()
        print("وظیفه با موفقیت اضافه شد!")
    except sqlite3.Error as e:
        print(e)


def show_tasks(conn):
    """نمایش تمام وظایف"""
    try:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT id, title, priority, 
               strftime('%Y-%m-%d %H:%M', created_at), 
               completed 
        FROM tasks
        ORDER BY priority, created_at
        """)

        print("\nلیست وظایف:")
        print("-" * 40)
        for task in cursor.fetchall():
            status = "✅" if task[4] else "❌"
            print(f"{task[0]}. [{status}] {task[1]} (اولویت: {task[2]}) - {task[3]}")
        print("-" * 40)
    except sqlite3.Error as e:
        print(e)


def complete_task(conn, task_id):
    """تکمیل کردن یک وظیفه"""
    try:
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE tasks SET completed = 1 
        WHERE id = ?
        """, (task_id,))
        conn.commit()
        print("وظیفه به عنوان تکمیل شده علامت زده شد!")
    except sqlite3.Error as e:
        print(e)


# اجرای اصلی برنامه
if __name__ == '__main__':
    conn = create_connection()
    if conn:
        setup_database(conn)

        while True:
            print("\n1. نمایش وظایف")
            print("2. اضافه کردن وظیفه جدید")
            print("3. تکمیل کردن وظیفه")
            print("4. خروج")

            choice = input("انتخاب شما: ")

            if choice == '1':
                show_tasks(conn)
            elif choice == '2':
                title = input("عنوان وظیفه: ")
                priority = input("اولویت (1-3): ")
                add_task(conn, title, int(priority))
            elif choice == '3':
                task_id = input("شناسه وظیفه: ")
                complete_task(conn, int(task_id))
            elif choice == '4':
                break
            else:
                print("گزینه نامعتبر!")

        conn.close()11