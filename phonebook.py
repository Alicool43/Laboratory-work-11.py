import psycopg2

DB_NAME = "postgres"
USER = "postgres"
PASSWORD = "Kausar5"
HOST = "localhost"
PORT = "5432"

def connect():
    return psycopg2.connect(
        database=DB_NAME, user=USER, password=PASSWORD, host=HOST, port=PORT
    )

def search_pattern(pattern):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM search_pattern(%s)", (pattern,))
    rows = cur.fetchall()
    conn.close()

    for row in rows:
        print(row)

def insert_or_update():
    name = input("Введите имя: ")
    phone = input("Введите телефон: ")

    conn = connect()
    cur = conn.cursor()
    cur.execute("CALL insert_or_update(%s, %s)", (name, phone))
    conn.commit()
    conn.close()

    print("Вставка/обновление выполнены!")

def insert_many():
    n = int(input("Сколько пользователей добавить?: "))
    users = []

    for _ in range(n):
        name = input("Имя: ")
        phone = input("Телефон: ")
        users.append([name, phone])

    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM insert_many_users(%s)", (users,))
    bad = cur.fetchall()

    conn.commit()
    conn.close()

    if bad:
        print("\n❌ Неверные данные:")
        for row in bad:
            print(row)
    else:
        print("\n✅ Все пользователи добавлены корректно!")

def pagination():
    limit = int(input("Введите limit: "))
    offset = int(input("Введите offset: "))

    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM get_page(%s, %s)", (limit, offset))
    rows = cur.fetchall()
    conn.close()

    for r in rows:
        print(r)

def delete_by_proc():
    value = input("Введите имя или телефон для удаления: ")

    conn = connect()
    cur = conn.cursor()
    cur.execute("CALL delete_by_name_or_phone(%s)", (value,))
    conn.commit()
    conn.close()

    print("✅ Запись удалена!")


def menu():
    while True:
        print("\n=== МЕНЮ PHONEBOOK ===")
        print("1 - Поиск по шаблону")
        print("2 - Вставить или обновить")
        print("3 - Массовая вставка")
        print("4 - Пагинация")
        print("5 - Удалить (процедура)")
        print("0 - Выход")

        choice = input("Ваш выбор: ")

        if choice == "1":
            pattern = input("Введите шаблон: ")
            search_pattern(pattern)

        elif choice == "2":
            insert_or_update()

        elif choice == "3":
            insert_many()

        elif choice == "4":
            pagination()

        elif choice == "5":
            delete_by_proc()


        elif choice == "0":
            break

        else:
            print("Неверный выбор!")


if __name__ == "__main__":
    menu()