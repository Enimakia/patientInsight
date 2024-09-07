import sqlite3


# Database setup
def setup_database():
    conn = sqlite3.connect('patient_records.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS patients
                 (id INTEGER PRIMARY KEY, name TEXT, age INTEGER, gender TEXT, 
                  location TEXT, symptoms TEXT, analysis TEXT, timestamp TEXT)''')
    conn.commit()
    return conn, c


def insert_patient_record(name, age, gender, location, symptoms, analysis, timestamp):
    conn, c = setup_database()
    c.execute("INSERT INTO patients (name, age, gender, location, symptoms, analysis, timestamp) VALUES (?, ?, ?, ?, "
              "?, ?, ?)",
              (name, age, gender, location, symptoms, analysis, timestamp))
    conn.commit()
    conn.close()
