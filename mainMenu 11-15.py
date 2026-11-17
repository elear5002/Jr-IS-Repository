import tkinter as tk
from main import conn,cur
def toggleSymp(s):
    if s[1]==True:
        s[1] = False
    else:
        s[1] = True
    print(s[0][1])
    print(s[1])
def logMGsymp(cmi):
    mgsympmenu = tk.Tk()
    mgsympmenu.geometry("600x700")
    mgsympmenu.configure(bg="green")


    cur.execute('select * from m_symptom')
    cc = cur.fetchall()
    for c in cc:
        print(c)

    msymp = ["Constipation", "Mood changes", "Food cravings", "Neck stiffness", "Frequent urination",
             "Frequent yawning",
             "Visual changes", "Vision loss", "Pins & Needles Feeling", "Weakness", "Numbness", "Trouble Speaking",
             "Pain in head or neck", "Nausea", "Vomiting", "Sensitivity to light", "Sensitivity to sound",
             "Sensitivity to smell", "fatigue", "brain fog"]
    for i in range(int(len(msymp))):
        cur.execute('insert or ignore into m_symptom values (?, ?)', ((i + 1), msymp[i]))
        conn.commit()
        print("success")
    cur.execute('select * from m_symptom')
    cc = cur.fetchall()



    symptomtracker = []
    t = 0
    for i in range(len(cc)):
        symptomtracker.append([cc[i], False])


    """
    mgattacklog.columnconfigure(2, weight=1)
    mgattacklog.columnconfigure(3, weight=1)
    mgattacklog.rowconfigure(0, weight=1)
    mgattacklog.rowconfigure(1, weight=1)
    mgattacklog.rowconfigure(2, weight=1)
    mgattacklog.rowconfigure(3, weight=1)
    mgattacklog.rowconfigure(4, weight=1)
    """
    for i in range(len(symptomtracker)):
        btn1 = tk.Button(mgsympmenu, text=symptomtracker[i][0][1], font=("Arial", 7), command=
        lambda i=i: toggleSymp(symptomtracker[i]))

        btn1.pack(pady=5)
    cur.execute('select migraine_attack_id from m_attack')
    voidd = cur.fetchall()
    current_migraine_attack = voidd[len(voidd)-1] + 1

    subbtn = tk.Button(mgsympmenu, text="submit", command=lambda:submitMigAttack(symptomtracker, current_migraine_attack))
    subbtn.pack()
    mgsympmenu.mainloop()



def submitMigAttack(symptomT, cmi):
    for i in range(symptomT):
        if (symptomT[i][1] == True):
            query = 'insert or ignore into m_attack_symptom values (?, ?)'
            vals = (symptomT[i][0][0], cmi)
            cur.execute(query, vals)
            conn.commit()



def logMigraineAttack():


    mgattacklog = tk.Tk()
    mgattacklog.geometry("600x600")

    global next_available_m_attack
    global current_user_id
    cur.execute('''
    select next_available_m_attack_id from next_availables

    ''')
    next_available_m_attack = cur.fetchone()
    mgattacklog.config(bg="green")
    ww = 50



    tk.Label(mgattacklog, text="Enter the start date of the attack as a string in the format 2026-11-19", bg="green").pack(pady=10)
    stdateentry = tk.Entry(mgattacklog, width=ww)
    stdateentry.pack()

    tk.Label(mgattacklog, text="Enter the end date of the attack as a string in the format 2026-11-19", bg="green").pack(pady=10)
    enddateentry = tk.Entry(mgattacklog, width=ww)
    enddateentry.pack()



    tk.Label(mgattacklog, text="Enter the start time of the attack as a string in the format 2026-11-19", bg="green").pack(pady=10)
    sttimeentry = tk.Entry(mgattacklog, width=ww)
    sttimeentry.pack()

    tk.Label(mgattacklog, text="Enter the end time of the attack as a string in the format 2026-11-19", bg="green").pack(pady=10)
    endtimeentry = tk.Entry(mgattacklog, width=ww)
    endtimeentry.pack()

    tk.Label(mgattacklog, text="Enter your pain level (0 is no pain and 10 is the worst headache of your life)", bg="green").pack(pady=10)
    endtimeentry = tk.Entry(mgattacklog, width=ww)
    endtimeentry.pack()
    cur.execute('delete from m_symptom')

    mgattacklog.mainloop()






def mainMenu():
    global current_user_id
    mainMenuM = tk.Tk()
    mainMenuM.geometry("600x600")
    mainMenuM.configure(bg="green")
    cur.execute('select * from m_attack')


    tk.Label(mainMenuM, text="What would you like to do?", fg="white", bg="green", font=("Arial, 28")).pack()
    tk.Button(mainMenuM, text="Log my migraine", fg="black", bg="green", font=("Arial, 28"), command=logMigraineAttack).pack()
    tk.Button(mainMenuM, text="See my migraine and sleep patterns", fg="black", bg="green", font=("Arial, 28"), command=logMigraineAttack).pack()
    tk.Button(mainMenuM, text="Log a night sleep", fg="black", bg="green", font=("Arial, 28"),command=logSleep).pack()
    tk.Button(mainMenuM, text="Log a period", fg="black", bg="green", font=("Arial, 28"), command=logPeriod).pack()


    mainMenuM.mainloop()

def saveSleep(sleeps, wakeups, sleepdate):
    cur.execute('select * from sleep')
    speels = cur.fetchall()
    newsleepid = speels[len(speels) -1][0]

    cur.execute('select * from sleep_cycle')
    scs = cur.fetchall()
    newsleepcid = scs[len(scs) - 1][0]

    cur.execute('insert or ignore into sleep values (sleep_id,patient_id,start_date) values (?,?, ?)', (newsleepid, current_user_id, sleepdate.get()))
    conn.commit()

    sleps = sleeps.get().split(",")
    wkups = wakeups.get().split(",")



    for i in range(len(sleps)):
        cur.execute('insert or ignore into sleep_cycle (sleep_cycle_id,sleep_id,start_time,end_time) values (?,?, ?, ?)', (newsleepcid + i + 1, newsleepid, sleps[i], wkups[i]))
        conn.commit()





def logSleep():
    cur.execute('select * from sleep')
    fetchal = cur.fetchall()
    ww = 50

    #newsleepid = fetchal[len(fetchal) -1][1]
    sleeptracker = tk.Tk()
    sleeptracker.configure(bg='blue')
    sleeptracker.geometry("600x600")

    tk.Label(sleeptracker, text="What is the date of the sleep you are logging?", bg="blue").pack(pady=10)
    sleepdate = tk.Entry(sleeptracker, width=ww)
    sleepdate.pack()

    tk.Label(sleeptracker, text="What time did you go to bed?", bg="blue").pack(pady=10)
    sttimeentry = tk.Entry(sleeptracker, width=ww)
    sttimeentry.pack()



    tk.Label(sleeptracker, text="What time did you get up?", bg="blue").pack(pady=10)
    endtimeentry = tk.Entry(sleeptracker, width=ww)
    endtimeentry.pack()

    tk.Label(sleeptracker, text="Name all the times you remember going to sleep between the time ", bg="blue").pack(pady=10)
    tk.Label(sleeptracker, text="you initially went to bed and the time you got up.",bg="blue").pack(pady=0)
    tk.Label(sleeptracker, text="Use the 24 hour clock. Separate each time with a comma. Do not use spaces. Ex: 23:20,1:30,4:50.", bg="blue").pack(pady=10)

    cyclestarts = tk.Entry(sleeptracker, width=ww)
    cyclestarts.pack()

    tk.Label(sleeptracker, text="Name all the times you remember aking up between the time ", bg="blue").pack(pady=10)
    tk.Label(sleeptracker, text="you initially went to bed and the time you got up.",bg="blue").pack(pady=0)

    tk.Label(sleeptracker, text="Use the 24 hour clock. Separate each time with a comma. Do not use spaces. Ex: 23:20,1:30,4:50.", bg="blue").pack(pady=10)
    tk.Label(sleeptracker, text="MAKE SURE YOU HAVE THE SAME AMOUNT OF START TIMES AS YOU DO END TIMES.", bg="blue").pack(pady=0)



    wakeups = tk.Entry(sleeptracker, width=ww)
    wakeups.pack()

    tk.Button(sleeptracker, text="submit", command=lambda:saveSleep(cyclestarts, wakeups,sleepdate) )
def submitPeriod(st, cpd):
    for i in range(len(st)):
        if st[i][1] == True:
            cur.execute('insert or ignore into p_attack_symptom (p_symptom_id,period_id) values (?, ?)', (st[i][0][0], cpd))
            conn.commit()



def saveperiod(stdate, endate, pid, cpd):
    if endate.get() == "":
        cur.execute('insert or ignore into period (period_id, patient_id, start_date, end_date) values (?,?,?,?)', (cpd, pid, stdate, None))
        conn.commit()
    else:
        cur.execute('insert or ignore into period (period_id, patient_id, start_date, end_date) values (?,?,?,?)',
                    (cpd, pid, stdate.get(), endate.get()))
        conn.commit()
    logPsymp(cpd)






def logPeriod():
    cur.execute('select * from period')
    fetchal = cur.fetchall()
    ww = 50

    newperiodid = fetchal[len(fetchal) -1][1]
    periodtracker = tk.Tk()
    periodtracker.configure(bg='blue')
    periodtracker.geometry("600x600")

    tk.Label(periodtracker, text="What day did your period start?", bg="blue").pack(pady=10)
    pdate = tk.Entry(periodtracker, width=ww)
    pdate.pack()

    tk.Label(periodtracker, text="What day did your period end?", bg="blue").pack(pady=10)
    tk.Label(periodtracker, text="Leave blank if ongoing", bg="blue").pack(pady=10)
    pendate = tk.Entry(periodtracker, width=ww)
    pendate.pack(pady=10)
    tk.Button(periodtracker, text="submit", command=lambda:saveperiod(pdate, pendate, newperiodid, current_user_id)).pack()

    periodtracker.mainloop()







def logPsymp(cpd):
    mgsympmenu = tk.Tk()
    mgsympmenu.geometry("600x700")
    mgsympmenu.configure(bg="green")

    cur.execute('select * from m_symptom')
    cc = cur.fetchall()
    for c in cc:
        print(c)


    symptomtracker = []
    t = 0
    for i in range(len(cc)):
        symptomtracker.append([cc[i], False])

    """
    mgattacklog.columnconfigure(2, weight=1)
    mgattacklog.columnconfigure(3, weight=1)
    mgattacklog.rowconfigure(0, weight=1)
    mgattacklog.rowconfigure(1, weight=1)
    mgattacklog.rowconfigure(2, weight=1)
    mgattacklog.rowconfigure(3, weight=1)
    mgattacklog.rowconfigure(4, weight=1)
    """
    for i in range(len(symptomtracker)):
        btn1 = tk.Button(mgsympmenu, text=symptomtracker[i][0][1], font=("Arial", 7), command=
        lambda i=i: toggleSymp(symptomtracker[i]))

        btn1.pack(pady=5)



    subbtn = tk.Button(mgsympmenu, text="submit",
                       command=lambda: saveperiod(symptomtracker, cpd))
    subbtn.pack()
    mgsympmenu.mainloop()


def submitMigAttack(symptomT, cmi):
    for i in range(symptomT):
        if (symptomT[i][1] == True):
            query = 'insert or ignore into m_attack_symptom values (?, ?)'
            vals = (symptomT[i][0][0], cmi)
            cur.execute(query, vals)
            conn.commit()


def seeMigraines(current_user_id):
    seeMigraineReport = tk.Tk()
    seeMigraineReport.configure(background="green")
    canv = tk.Canvas(seeMigraineReport)
    scrollbar = tk.Scrollbar(seeMigraineReport, orient= "vertical", command=canv.yview)
    canv.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    canv.pack(side="left", fill="both", expand=True)

    scrollable_frame = tk.Frame(canv)
    canv.create_window((0, 0), window=scrollable_frame, anchor="nw")


    scrollable_frame.bind(
        "<Configure>",
        lambda e: canv.configure(scrollregion=canv.bbox("all"))
    )

    # 4. Add your widgets to scrollable_frame (not root)
    for i in range(30):
        tk.Label(scrollable_frame, text=f"Item {i + 1}").pack(pady=5)

    # Optional: Enable mousewheel scrolling (Windows/macOS)
    canv.bind_all("<MouseWheel>", lambda e: canv.yview_scroll(int(-1 * (e.delta / 120)), "units"))

    cur.execute('select * from m_attack where patient_id = ?', (current_user_id,))
    migs = cur.fetchall()
    cur.execute('select * from m_attack_symptom mas join m_symptom ms on mas.m_symptom_id = ms.symptom_id')
    msys = cur.fetchall()
    cur.execute('select * from m_attack_pain_type mapt join m_pain_type mpt on mapt.m_pain_type_id = mpt.m_pain_type_id')
    mappt = cur.fetchall()





    for m in migs:
        tk.Label(seeMigraineReport, text="Start date: " + m[2] + ", end date:" + m[3] + ", start time: "+ m[4] + ", end time: " + m[5], font=("Arial", 18)).pack()
        tk.Label(seeMigraineReport,text="Symptoms", font=("Arial", 18)).pack()
        for ms in msys:
            if (ms[0] == m[0]):
                tk.Label(seeMigraineReport, text=msys[3], font=("Arial", 18)).pack()
        for mapp in mappt:
            if mapp[1] == m[0]:
                tk.Label(seeMigraineReport, text=msys[3], font=("Arial", 18)).pack()
    seeMigraineReport.mainloop()







def seePeriods(current_user_id):
    seeMigraineReport = tk.Tk()

    cur.execute('select * from m_attack where patient_id = ?', (current_user_id,))
    migs = cur.fetchall()
    for m in migs:
        tk.Label(seeMigraineReport,
                 text="Start date: " + m[2] + ", end date:" + m[3] + ", start time: " + m[4] + ", end time: " + m[5],
                 font=("Arial", 18))

def seeMGTrendsReport(current_user_id):
    seeMigraineReport = tk.Tk()
    seeMigraineReport.configure(background="green")
    tk.Label()
    
    
    
