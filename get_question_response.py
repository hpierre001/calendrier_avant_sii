import time
import json
import datetime as dt

from CalendrierAvant import CalendrierAvant

if __name__ == "__main__":
    
    try:
        with open("mails.txt", "r") as f:
            mails = f.readlines()
    except OSError:
        mails = []
    
    filename_response = "reponse.json"
    with open(filename_response, 'r', encoding='utf-8') as f:
        question_reponse = json.load(f)
    
    # Pour les lundi
    was_week_end = False
    
    day = dt.date.today().day
    days = range(day-2, day+1) if was_week_end else [day]

    calendrier_avant = None
    for mail in mails:
        if calendrier_avant is None:
            calendrier_avant = CalendrierAvant()
        try:
            calendrier_avant.login(mail)
        except Exception as ex:
            print(ex)
            continue
        
        for day in days:
            try:
                question_reponse.update(calendrier_avant.quiz(day, question_reponse))
            except Exception as ex:
                print(ex)
                continue
        
        try:
            calendrier_avant.logout()
        except Exception as ex:
            print(ex)
            try:
                calendrier_avant.close()
            except:
                pass
            finally:
                calendrier_avant = None
    
    if calendrier_avant:
        calendrier_avant.close()
    
    with open(filename_response, 'w', encoding='utf-8') as f:
        json.dump(question_reponse, f, indent=4, ensure_ascii=False, sort_keys=True)