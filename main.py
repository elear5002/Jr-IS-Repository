# This is a sample Python script.

import sqlite3
next_available_patient = 1
conn = sqlite3.connect('jr iss.db')
user_name = ""
password = ""
next_available_m_attack = 1

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
cur = conn.cursor()





            


def showMenu():
    print("1. sign up")
    print("2. login")
    print("3. see all attacks")
    print("4. see all patients")
    choice = int(input("Enter your choice: "))
def handleChoice(choice):
    if choice == 1:
        signup()
    elif choice == 2:
        login()
    #elif choice == 3:



def login():
    username = input("Enter your username: ")
    #cur.execute("SELECT username FROM patient WHERE username = ?", username)
    password = input("Enter your password: ")


def signup():
    global next_available_patient
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    age = input("Enter your age: ")
    dob = input("Enter your date of birth: ")
    cur.execute('''
        insert into patient (username, password, patient_id, age, dob) values (?, ?, ?, ?, ?)
    ''', (username, password,  next_available_patient, age, dob))

    conn.commit()
    next_available_patient += 1

def createTables():
    cur.execute('''
        create table if not exists patient (
            username text not null,
            password text not null,
            patient_id integer not null primary key,
            age integer not null,
            dob date not null
        )
    ''')
    conn.commit()

    cur.execute('''
            create table if not exists m_attack (
                migraine_attack_id integer primary key not null,
                patient_id integer not null,
                start_date datetime not null,
                end_date datetime
            )
        ''')
    conn.commit()

    cur.execute('''
                create table if not exists m_symptom (
                    m_symptom_id integer primary key not null,
                    symptom_name text not null
                    
                )
            ''')
    conn.commit()

    cur.execute('''
                create table if not exists gender ( 
                    gender_id integer primary key not null,
                    gender_name text not null
                )
                ''')
    conn.commit()

    cur.execute('''
                    create table if not exists gender ( 
                        gender_id integer primary key not null,
                        gender_name text not null
                    )
                    ''')
    conn.commit()
    gender_query = "insert or ignore into gender (gender_id, gender_name) values (?, ?)"
    genders = [(1, "Male"), (2, "Female"), (3, "Non-binary"), (4, "Prefer not to say")]
    conn.executemany(gender_query, genders)
    conn.commit()
    cur.execute('''
                    create table if not exists m_attack_symptom ( 
                        migraine_attack_id int primary key not null,
                        m_symptom_id integer not null
                        
                    )
                    ''')
    conn.commit()


    cur.execute('''
                    create table if not exists m_pain_scale ( 
                        m_pain_level integer not null
                    )
                ''')
    conn.commit()

    pain_query = "insert or ignore into m_pain_scale (m_pain_level) values (?)"
    for i in range(11):
        conn.execute(pain_query, [i])
    conn.commit()
    """
    cur.execute('''
                    create table if not exists m_pain_type ( 
                    
                ''')
"""














createTables()
print("")
