import tkinter as tk
from main import conn,cur
import numpy
import datetime


def toggleSymp(s):
    if s[1]==True:
        s[1] = False
    else:
        s[1] = True
    print(s[0][1])
    print(s[1])

#Allows patients to log migraine symptoms
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


#saves a migraine attack to the database
def submitMigAttack(symptomT, cmi):
    for i in range(symptomT):
        if (symptomT[i][1] == True):
            query = 'insert or ignore into m_attack_symptom values (?, ?)'
            vals = (symptomT[i][0][0], cmi)
            cur.execute(query, vals)
            conn.commit()

#saves a migraine attack to the database
def sumbitMigAttackk(sde, ede, ste, ete, ple, current_user_id):
    cur.execute('''
        select migraine_attack_id from m_attack


        ''')
    next_available_m_attack = cur.fetchall()[len(cur.fetchall()) - 1] + 1
    cur.execute('insert or ignore into m_attack (migraine_attack_id,patient_id,start_date,end_date,start_time,end_time) values (?,?,?,?,?,?)', (next_available_m_attack, current_user_id, sde.get(), ede.get(), ste.get(), ete.get()))

#allows a usert to log a pigraine attack
def logMigraineAttack():


    mgattacklog = tk.Tk()
    mgattacklog.geometry("600x600")

    global next_available_m_attack
    global current_user_id

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
    plentry = tk.Entry(mgattacklog, width=ww)
    plentry.pack()

    tk.Button(mgattacklog, text="Submit", bg="gray", command=lambda: sumbitMigAttackk(stdateentry, enddateentry, sttimeentry, endtimeentry, plentry)).pack(pady=10)

    mgattacklog.mainloop()








#main menu that shows after user is logged in
def mainMenu(current_user_id):


    mainMenuM = tk.Tk()
    mainMenuM.geometry("600x600")
    mainMenuM.configure(bg="green")
    cur.execute('select * from m_attack')


    tk.Label(mainMenuM, text="What would you like to do?", fg="white", bg="green", font=("Arial", 28)).pack()
    tk.Button(mainMenuM, text="Log my migraine", fg="black", bg="green", font=("Arial", 28), command=logMigraineAttack).pack()
    tk.Button(mainMenuM, text="See my migraine and sleep patterns", fg="black", bg="green", font=("Arial", 28), command=lambda: seeMGTrendsReport(current_user_id)).pack()
    tk.Button(mainMenuM, text="Log a night sleep", fg="black", bg="green", font=("Arial", 28),command=lambda: logSleep(current_user_id)).pack()
    tk.Button(mainMenuM, text="See sleep patterns", fg="black", bg="green", font=("Arial", 28), command=lambda: seeSleepreport(current_user_id)).pack()
    tk.Button(mainMenuM, text="Log a period", fg="black", bg="green", font=("Arial", 28), command=logPeriod).pack()




    mainMenuM.mainloop()
#returns to main menu after patient is logged in
def returnToMainMenu(prevView, current_user_id):
    mainMenu(current_user_id)
    prevView.destroy()
#saves a sleep episode to the database
def saveSleep(sleeps, wakeups, sleepdate, current_user_id):
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




#allows a patient to log a night's sleep
def logSleep(current_user_id):
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
#saves a period to the database
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





#allows a patient to log their period
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






#allows a patient to log their period symptoms
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

#logs a migraine attack to the database
def submitMigAttack(symptomT, cmi):
    for i in range(symptomT):
        if (symptomT[i][1] == True):
            query = 'insert or ignore into m_attack_symptom values (?, ?)'
            vals = (symptomT[i][0][0], cmi)
            cur.execute(query, vals)
            conn.commit()


def seeMigraines(current_user_id):
    #allows user to see their migraine attacks






    cur.execute('select * from m_attack where patient_id = ?', (current_user_id,))
    migs = cur.fetchall()
    cur.execute('select * from m_attack_symptom mas join m_symptom ms on mas.m_symptom_id = ms.symptom_id join m_attack ma on mas.migraine_attack_id = ma.migraine_attack_id where ma.patient_id = ?', (current_user_id,))
    msys = cur.fetchall()
    cur.execute('select * from m_attack_pain_type mapt join m_pain_type mpt on mapt.m_pain_type_id = mpt.m_pain_type_id')
    mappt = cur.fetchall()

    for ms in msys:
        print(ms)









    for m in migs:
        print("Migraine start date: ")
        print(m[2])
        print("Migraine end date: ")
        print(m[3])
        print("Migraine start time: ")
        print(m[4])
        print("Migraine end time: ")
        print(m[5])
        print("-----------")






seeMigraines(3)





#allows user to see their period
def seePeriods(current_user_id):
    seeMigraineReport = tk.Tk()

    cur.execute('select * from m_attack where patient_id = ?', (current_user_id,))
    migs = cur.fetchall()
    for m in migs:
        print("Start date: " + m[2])

        tk.Label(seeMigraineReport,
                 text="Start date: " + m[2] + ", end date:" + m[3] + ", start time: " + m[4] + ", end time: " + m[5],
                 font=("Arial", 18))
def analyzeMigraine():
    findAvgMigStTime()

#finds average start time for a migraine
def findAvgMigStTime(current_user_id):
    cur.execute('''
        select avg(unixepoch('1970-01-01' || start_time)) from m_attack where patient_id = ?

        ''', (current_user_id,))

    sts = cur.fetchall()



    average = numpy.mean(sts)

    haves = []
    have_nots = []

    for i in range(len(sts)):
        d = sts[i][0] - average
        if (d < 7200):
            haves.append(d)
        else:
            have_nots.append(d)

    return datetime.timedelta(seconds=numpy.round(average))





#finds the avergage end time for a migraine
def findAvgMigEndTime(current_user_id):
    cur.execute('''
            select avg(unixepoch('1970-01-01' || end_time)) from m_attack where patient_id = ?

            ''', (current_user_id,))

    sts = cur.fetchall()

    average = numpy.mean(sts)

    haves = []
    have_nots = []

    for i in range(len(sts)):
        d = sts[i][0] - average
        if (d < 7200):
            haves.append(d)
        else:
            have_nots.append(d)

    return datetime.timedelta(seconds=numpy.round(average))
"""
def findNormalSyptoms(current_user_id):


    cur.execute('''
    select mas.migraine_attack_id, ms.symptom_name from m_attack_symptom mas
    join m_symptom ms on mas.m_symptom_id = ms.m_symptom_id
    join m_attack ma on mas.migraine_attack_id = ma.migraine_attack_id
    where patient_id = ?
    ''', (current_user_id))

    allsymptoms = cur.fetchall()
    uniquemids = []
    uniquesymptoms = []
    normalsymptoms = []
    for i in range(len(allsymptoms)):
        if (allsymptoms[i][1] not in uniquesymptoms):
            uniquesymptoms.append(allsymptoms[i][1])
    symptomsbasedonmid = []
    for i in range(len(allsymptoms)):
        if allsymptoms[i][0] not in uniquemids:
            uniquemids.append(allsymptoms[i][0])
    for un in uniquemids:
        s = []
        for al in allsymptoms:
            if al[0] == un:
                s.append(al[1])
        symptomsbasedonmid.append(s)
    for sy in uniquesymptoms:
        haves = 0
        have_nots = 0

        for sym in symptomsbasedonmid:
            for sympt in sym:
                if sy == sympt:
                    haves += 1
                else:
                    have_nots += 1
        if (haves > have_nots):
            normalsymptoms.append(sym)
    return normalsymptoms
    """
#analyzes migraine trends
def seeMGTrendsReport(current_user_id):
    seeMigraineReport = tk.Tk()
    seeMigraineReport.configure(background="green")
    seeMigraineReport.geometry("600x600")
    #ns = findNormalSyptoms(current_user_id)
    py = 20

    cur.execute('select count(migraine_attack_id) from m_attack where patient_id = ?', (current_user_id,))
    nextText = "You've logged " + str(cur.fetchone()[0]) + " migraine episodes"
    tk.Label(seeMigraineReport, text= nextText, font=("Arial", 15), bg='green').pack(pady=py)

    tk.Label(seeMigraineReport, text="Average Start time:", font=("Arial", 15), bg='green').pack(pady=py)
    averageStTime = findAvgMigStTime(current_user_id)

    tk.Label(seeMigraineReport, text=averageStTime, font=("Arial", 15), bg='green').pack(pady=py)

    averageEndTime = findAvgMigEndTime(current_user_id)
    tk.Label(seeMigraineReport, text="Average Start time:", font=("Arial", 15), bg='green').pack(pady=py)

    tk.Label(seeMigraineReport, text=averageEndTime, font=("Arial", 15), bg='green').pack(pady=py)
    averageEndTime = findAvgMigEndTime(current_user_id)

    cur.execute('''
        select unixepoch(start_date) from period
        where patient_id = ?

        ''', (current_user_id,))

    pmaster = cur.fetchall()

    psds = []
    peds = []
    pids = []
    for row in pmaster:
        psds.append(row[0])

    cur.execute('''
        select unixepoch(start_date), unixepoch(end_date) from m_attack
        where patient_id = ?

        ''', (current_user_id,))

    msds = []
    meds = []


    mmaster = cur.fetchall()
    for mm in mmaster:
        msds.append(mm[0])
        meds.append(mm[1])

    haves = 0
    have_nots = 0

    for psd in psds:
        for i in range(len(meds)):
            if meds[i] != None and msds[i] != None:

                if meds[i] > psd and msds[i] < psd:
                    haves += 1
                else:
                    have_nots += 1
    if (haves >= have_nots):
        tk.Label(seeMigraineReport, text="You tend to have migraine episodes around your period", font=("Arial", 15), bg='green').pack(pady=py)
    tk.Button(seeMigraineReport, text="Return to Main Menu", font=("Arial", 15), bg='gray', command=lambda:returnToMainMenu(seeMigraineReport)).pack(pady=py)









    """









    for mig in msds:
        isAMigraine = False
        for date in intervdates:
            if intervdates[0] <= mig <= intervdates[1]:
                isAMigraine = True
                haves += 1
                break
        if not isAMigraine:
            have_nots += 1
    if haves > have_nots:
        tk.Label(seeMigraineReport, text=averageEndTime, font=("Arial", 15), bg='green').pack(pady=py)
    """





    seeMigraineReport.mainloop()
#analyzes sleep trends
def seeSleepreport(current_user_id):
    sleepReport = tk.Tk()
    sleepReport.configure(background='blue')
    sleepReport.geometry("600x600")


    cur.execute('select count(sleep_id) from sleep where patient_id = ?', (current_user_id,))
    sleepcount = cur.fetchone()[0]
    tk.Label(sleepReport, text="You have logged " + str(sleepcount) + " nights of sleep", bg='blue', font=("Arial", 20)).pack()
    print(sleepcount)

    cur.execute('''
        select avg(cycle_count) from (select count(sc.sleep_cycle_id) as cycle_count from sleep_cycle sc join sleep s on sc.sleep_id = s.sleep_id where s.patient_id = ? group by sc.sleep_id
        )
    ''', (current_user_id,))

    average = cur.fetchone()[0]
    print(int(average))
    tk.Label(sleepReport, text="You have an average of " + str(average) + " sleep cycle(s) per night"  , bg='blue',font=("Arial", 20)).pack()

    cur.execute("select unixepoch(s.start_date) from sleep s where patient_id = ?", (current_user_id,))
    sleepdates = cur.fetchall()
    for sd in sleepdates:

        print(sd[0])












    sleepReport.mainloop()
#shows sleep cycles and nights sleeps
def seeSleep(current_user_id):
    sleepCenter = tk.Tk()
    sleepCenter.configure(bg='blue')
    sleepCenter.geometry("600x600")
    cur.execute(
        'select count(sleep_id) from sleep s where patient_id = ?', (current_user_id,))
    tk.Label(sleepCenter, text="You logged " + str(cur.fetchone()[0]) + " nights of sleep").pack(pady=20)

    cur.execute(
        'select count(sc.sleep_cycle_id) from sleep_cycle sc join sleep s on sc.sleep_id =  s.sleep_id where patient_id = ?', (current_user_id,))
    tk.Label(sleepCenter, text="You logged " + str(cur.fetchone()[0]) + " sleep cycles").pack(pady=20)

    tk.Label(sleepCenter, text="Look at console to see all of your sleep cycles").pack(pady=20)

    cur.execute('select s.start_date, sc.start_time, sc.end_time from sleep s join sleep_cycle sc on s.sleep_id = sc.sleep_id where patient_id = ? group by s.sleep_id', (current_user_id,))




    sleeps = cur.fetchall()

    for sleep in sleeps:

        print(sleep)

    tk.Button(sleepCenter, text="Return to main menu", font=("Arial", 28), command=lambda: returnToMainMenu(sleepCenter, current_user_id)).pack(pady=20)
    sleepCenter.mainloop()







#seeSleepreport(1)

seeSleep(1)














#mainMenu()
#seeMigraines(1)
#seeMGTrendsReport(3)


#logMGsymp(1)



