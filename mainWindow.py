



from main import cur, conn
import tkinter as tk
from mainMenu import mainMenu
from tkinter import *
from loginpagepy import *
#initializes starting window
mainWindow = Tk()
mainWindow.geometry("600x600")
mainWindow.title("Auth Page")
username = ""
password = ""
cur.execute('delete from goals')
goals = ["track my migraines", "track my sleep", "look for patterns in relation to migraine and sleep",
         "look for patterns in relation to migraine and period",
         "look for patterns in relation to period and sleep", "track my period"]

for i in range(len(goals)):
    conn.execute('''
    insert or ignore into goals (goal_id, goal_name) values (?,?)

    ''', (i + 1, goals[i]))
    conn.commit()

cur.execute('select username from patient')
usernnn = cur.fetchall()
for usern in usernnn:
    print(usern)
#switches the value of a boolean variable
def toggle(val):
    if val == True:
        val = False
    else:
        val = True
    print(val)

#allows user to change their goals
def setGoals(genid, pid):
    goalpg = tk.Tk()
    goalpg.geometry("600x600")
    goalpg.config(background='blue')
    tk.Label(goalpg, text="What are your goals?", bg='green').pack(pady=10)
    trackmymigraines= False
    trackmysleep = False
    trackpatternsmas = False
    trackpatternsmap = False
    trackpatternspas = False
    trackp = False
    tk.Button(goalpg, text="track my migraines", font=('Arial', 18),
              command=lambda: toggle(trackmymigraines)).pack()

    tk.Button(goalpg, text="track my sleep", font=('Arial', 18),
              command=lambda: toggle(trackmysleep)).pack()

    tk.Button(goalpg, text="track my patterns related to migraine and sleep", font=('Arial', 18),
              command=toggle(trackpatternsmas)).pack()


    tk.Button(goalpg, text="track my patterns related to migraine and period", font=('Arial', 18),
            command=lambda: toggle(trackpatternsmap)).pack()

    tk.Button(goalpg, text="track my patterns related to period and sleep", font=('Arial', 18),
            command=lambda: toggle(trackpatternspas)).pack()

    tk.Button(goalpg, text="track my periods", font=('Arial', 18),
            command=lambda: toggle(trackp)).pack()
    cur.execute('delete from patient_goal where patient_id = ?', (pid,))
    cur.execute('delete from patient where username = ?', ('em0gurl2',))
    #saves goals to database
    def saveGoals():
        if (trackmymigraines):
            cur.execute('insert into patient_goal (patient_id, goal_id) values (?,?)', (pid, 1))
        if (trackmysleep):
            cur.execute('insert into patient_goal (patient_id, goal_id) values (?,?)', (pid, 2))
        if (trackpatternsmas):
            cur.execute('insert into patient_goal (patient_id, goal_id) values (?,?)', (pid, 3))
        if (trackpatternsmap):
            cur.execute('insert into patient_goal (patient_id, goal_id) values (?,?)', (pid, 4))
        if (trackpatternspas):
            cur.execute('insert into patient_goal (patient_id, goal_id) values (?,?)', (pid, 5))
        if (trackpatternsmap):
            cur.execute('insert into patient_goal (patient_id, goal_id) values (?,?)', (pid, 6))
        print('goals saved')
        mainMenu(pid)





    tk.Button(goalpg, text="submit", font= ('Arial', 18), bg='gray', command = lambda: saveGoals).pack()






mainWindow.config(background = "white")
mainPageT = tk.Label(mainWindow, text="Welcome!", font=('Arial', 18))
mainPageT.pack(padx = 20, pady=100)


buttonframe = tk.Frame(mainWindow)
buttonframe.columnconfigure(0,weight=1)
buttonframe.columnconfigure(1,weight=1)
buttonframe.columnconfigure(0,weight=1)
#logs the user in based on what they put in the boxes
def getlogin(usernameBox, passBox):
    global username
    global password
    username = usernameBox.get()
    password = passBox.get()
    print("Logged in")


    cur.execute("SELECT username, password, patient_id FROM patient")

    global current_user_id
    global current_user_gender





    upass = cur.fetchall()
    for i in range(len(upass)):
        if upass[i][0] == username:
            if upass[i][1] == password:
                print("Login successful")
                current_user_id = int(upass[i][2])
                break
            elif (upass[i][1] != password):
                print("username and password do not match")
                print("Try again")

                login()
                break
        elif upass[i][0] != username and i == len(upass) - 1:
            print("Login unsuccessful")
            print("Try again")

            login()
            break

    cur.execute('''
    select gender_id, patient_id from patient_gender where patient_id = ?
    ''', (int(current_user_id),))
    pg = cur.fetchall()

    current_user_gender = int(pg[0][0])
    mainMenu(current_user_id)



#allows user to put in info to log in
def login():
    isCorrect = True
    lgwindow = tk.Tk()
    lgwindow.geometry("600x600")
    lgwindow.title("Login Page")
    lgwindow.config(background='green')
    userLabel = tk.Label(lgwindow, text="Welcome back!", font=("Arial", 30))
    userLabel.pack()
    userLabel = tk.Label(lgwindow, text="Username:", font=("Arial",30))
    userLabel.pack(pady=20)

    usernameBox = Entry(lgwindow, font=("Arial", 28))
    usernameBox.pack(pady=10)
    userLabel = tk.Label(lgwindow, text="Password:", font=("Arial", 30))
    userLabel.pack(pady=20)


    passBox = Entry(lgwindow, font=("Arial", 28))
    passBox.pack()

    lgsubmitbtn = Button(lgwindow, text="sumbit", command=lambda: getlogin(usernameBox, passBox))

    lgsubmitbtn.pack()

    lgwindow.mainloop()


    mainWindow.destroy()









    #loginMenu()
lgbtn = tk.Button(buttonframe, text="Log in", font=('Arial', 18), fg='#066b01', command=login)

lgbtn.grid(row=3, column=0, sticky=tk.W+tk.E)
"""
def modify_goals(current_user_id):
    cur.execute('''
    delete from patient_goal
    where patient_id = ?

    ''', (current_user_id,))
    print("What are your goals?")
    cur.execute('''

    select * from goals

    ''')

    go = cur.fetchall()

    for g in go:
        print(g[0], g[1])
    print("Enter the number corresponding to each of your goals in the following format:")
    print("1,2,3,4,6")
    pgs = input("")

    toinput = pgs.split(",")
    for i in toinput:
        cur.execute('''

        insert or ignore into patient_goal values (?,?)
        ''', (current_user_id, i))
"""
#puts sign up info into database
def getsu(usernameBox, passBox, agebox, dobox, genderbox):
    username = usernameBox.get()
    password = passBox.get()
    age = agebox.get()
    dob = dobox.get()
    gender= genderbox.get()
    print(username)
    print(password)
    cur.execute('select patient_id from patient')
    pids = cur.fetchall()
    print(pids)


    next_available_patient = int(pids[len(pids)-1][0]) + 1
    print(password)
    cur.execute('select username from patient')
    pids = cur.fetchall()
    print(pids)


    cur.execute(''' insert into patient (username, password, patient_id, age, dob) values (?, ?, ?, ?, ?)
        ''', (username, password, next_available_patient, age, dob))
    conn.commit()
    cur.execute(''' insert into patient_gender(patient_id, gender_id) values(?, ?)

    ''', (next_available_patient, gender))
    conn.commit()



    print("sing up succesful")
    setGoals(genderbox.get(), next_available_patient)



#allows user to put info into database
def signup():



    global next_available_patient
    cur.execute('''select * from patient''')
    popopop = cur.fetchall()
    next_available_patient = popopop[len(popopop) -1][2]

    suwindow = tk.Tk()
    suwindow.geometry("600x900")
    suwindow.title("Login Page")
    suwindow.config(background='blue')
    userLabel = tk.Label(suwindow, text="Welcome!", font=("Arial", 30))
    userLabel.pack()
    userLabel = tk.Label(suwindow, text="Username:", font=("Arial", 30))
    userLabel.pack(pady=5)

    usernameBox = Entry(suwindow, font=("Arial", 28))
    usernameBox.pack(pady=5)
    userLabel = tk.Label(suwindow, text="Password:", font=("Arial", 30))
    userLabel.pack(pady=5)

    passBox = Entry(suwindow, font=("Arial", 28))
    passBox.pack()

    ageLabel = tk.Label(suwindow, text="Age:", font=("Arial", 30))
    ageLabel.pack()
    ageBox = Entry(suwindow, font=("Arial", 28))
    ageBox.pack(pady=5)

    DOBLABEL = tk.Label(suwindow, text="Date of Birth:", font=("Arial", 30))
    DOBLABEL.pack(pady=5)
    DOBLABEL2 = tk.Label(suwindow, text="Put in YYYY-MM-DD format", font=("Arial", 20))
    DOBLABEL2.pack(pady=5)
    DOBox = Entry(suwindow, font=("Arial", 28))
    DOBox.pack(pady=5)


    genderlabel = tk.Label(suwindow, text="Type the number thay corresponds to your sex/gender: ", font=("Arial", 15))
    genrelabel = tk.Label(suwindow, text="1 - male, 2 - female, 3 - non - binary, 4 -, prefer not to say", font=("Arial", 15))
    genderlabel.pack(pady=5)
    genrelabel.pack(pady=0)
    genderbox = Entry(suwindow, font=("Arial", 28))
    genderbox.pack(pady=5)






    cur.execute("select * from goals")
    goall = IntVar()


    go = cur.fetchall()
    for g in go:
        print(g)









    susubmitbtn = Button(suwindow, text="sumbit", command=lambda: getsu(usernameBox, passBox, ageBox, DOBox, genderbox))

    susubmitbtn.pack()



    mainWindow.destroy()

    suwindow.mainloop()












subtn = tk.Button(buttonframe, text="Sign Up", font=('Arial', 18), fg='#0a0ef2', command=signup)
subtn.grid(row=4, column=0, sticky=tk.W+tk.E)

buttonframe.pack()

mainWindow.mainloop()























mainMenu(1)
















mainMenu(1)
