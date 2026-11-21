from main import conn, cur, createTables

cur.execute('delete from m_attack')
cur.execute('delete from m_attack_symptom')
cur.execute('delete from m_attack_pain_type')
cur.execute('delete from period')
cur.execute('delete from p_attack_symptom')
cur.execute('delete from sleep')
cur.execute('delete from sleep_cycle')
cur.execute('delete from patient_goal')


with open(".venv/synthetic_migraine_dataset_6_patients-2.sql", "r", encoding="utf-8") as dset:
    sampleset = dset.read()
cur.executescript(sampleset)
conn.commit()
