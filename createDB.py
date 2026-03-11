import sqlite3

def main():
    conn = sqlite3.connect("enano.db")
    cursor = conn.cursor()
    with open("createDB.sql", "r") as file:
        sql_script = file.read()
    cursor.executescript(sql_script)
    conn.close()
    print("Database created succesfully")

if __name__ == "__main__":
    main()