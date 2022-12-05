import json
import datetime as dt

from CalendrierAvant import CalendrierAvant

if __name__ == "__main__":
    
    try:
        from my_id import *
    except:
        mail = ""
        password = ""

    # Pour les lundi
    was_week_end = False
    
    day = dt.date.today().day
    days = range(day-2, day+1) if was_week_end else [day]

    filename_response = "reponse.json"
    with open(filename_response, 'r', encoding='utf-8') as f:
        question_reponse = json.load(f)

    calendrier_avant = CalendrierAvant()
    try:
        calendrier_avant.login(mail, password)
        for day in days:
            try:
                question_reponse.update(calendrier_avant.quiz(day, question_reponse, True))
            except Exception as ex:
                print(ex)
                continue
        calendrier_avant.logout()
        calendrier_avant.close()
    except Exception as ex:
        print(ex)
    
    with open(filename_response, 'w', encoding='utf-8') as f:
        json.dump(question_reponse, f, indent=4, ensure_ascii=False, sort_keys=True)