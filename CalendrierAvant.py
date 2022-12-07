import random as rd
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import my_expected_conditions as myEC


class CalendrierAvant:

    url = "https://christmasbysii.com/"

    def __init__(self, timeout=20, poll_frequency=.1) -> None:
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.action = ActionChains(self.driver)
        self.wait = WebDriverWait(self.driver, timeout=timeout, poll_frequency=poll_frequency)
        self.timeout = timeout

        self.driver.get(self.url)

    def login(self, mail, password="azerty"):
        self.wait.until(EC.presence_of_element_located((By.XPATH, ".//login")))
        mail_input = self.driver.find_element(By.XPATH, ".//input[@formcontrolname='mail']")
        mail_input.send_keys(mail)
        mail_input.send_keys(Keys.ENTER)

        password_input = self.driver.find_element(By.XPATH, ".//input[@formcontrolname='password']")
        password_input.send_keys(password)
        password_input.send_keys(Keys.ENTER)

        self.wait.until(EC.presence_of_element_located((By.XPATH, ".//div[@class='ctr-page-avent ng-star-inserted']")))

    def logout(self):
        self.wait.until(EC.presence_of_element_located((By.XPATH, ".//div[@class='ctr-page-avent ng-star-inserted']")))
        
        btn_more_vert = self.wait.until(EC.element_to_be_clickable((By.XPATH, ".//mat-icon[text()='more_vert']")))
        self.action.move_to_element(btn_more_vert)
        self.action.click(btn_more_vert)
        self.action.perform()
        
        btn_deconect = self.wait.until(EC.element_to_be_clickable((By.XPATH, ".//button[@class='w-100 mat-raised-button mat-button-base mat-warn']")))
        self.action.move_to_element(btn_deconect)
        self.action.click(btn_deconect)
        self.action.perform()
        
        btn_confirm = self.wait.until(EC.element_to_be_clickable((By.XPATH, ".//button[@class='mat-raised-button mat-button-base mat-primary ng-star-inserted']")))
        self.action.move_to_element(btn_confirm)
        self.action.click(btn_confirm)
        self.action.perform()

        self.wait.until(EC.presence_of_element_located((By.XPATH, ".//login")))

    def quiz(self, day_num, question_reponse: dict = None, human: bool = False, real_human: bool = False):
        # Case du jour
        day_case = self.wait.until(myEC.element_located_is_steady((By.XPATH, f".//div[div[@class='numero' and contains(@style, 'img/avent/{day_num}.png')]]")))
        self.action.move_to_element(day_case)
        self.action.click(day_case)
        self.action.perform()

        # Lancer le quizz
        self.wait.until(myEC.element_located_is_steady((By.XPATH, f".//quiz-avent")))
        launch_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, ".//button[@class='mat-raised-button mat-button-base mat-primary']")))
        self.action.move_to_element(launch_btn)
        self.action.click(launch_btn)
        self.action.perform()

        reponse = None
        if question_reponse:
            question = self.wait.until(EC.presence_of_element_located((By.XPATH, ".//div[@class='question']/span"))).text
            try:
                reponse = question_reponse[question]
                ans_btn_xpath = f".//button[.//div[text()='{reponse}']]"
            except KeyError:
                ans_btn_xpath = ".//button[@class='mat-raised-button mat-button-base encours ng-star-inserted']"
        else:
            ans_btn_xpath = ".//button[@class='mat-raised-button mat-button-base encours ng-star-inserted']"

        # Bouton réponse
        if not human or reponse:
            ans_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, ans_btn_xpath)))

            # Make bots sleeping a random time between 1 and 8 seconds to avoid too good or too bad scores
            if not human:
                time.sleep(rd.random()*7)
            elif real_human:
                time.sleep(rd.random())

            self.action.move_to_element(ans_btn)
            self.action.click(ans_btn)
            self.action.perform()
        
        # Bouton récapitulatif
        to_ans_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, ".//button[@class='mat-raised-button mat-button-base mat-primary']")))
        self.action.move_to_element(to_ans_btn)
        self.action.click(to_ans_btn)
        self.action.perform()

        # Récupération de la question et de la réponse
        recap_question = self.wait.until(EC.presence_of_element_located((By.XPATH, ".//div[@class='recapitulatif-question-detail']")))
        question = recap_question.find_element(By.CLASS_NAME, "question").text
        reponse = recap_question.find_element(By.XPATH, ".//div[@class='reponse-result reponse-ok ng-star-inserted']/span").text

        # Quitte le pop up
        exit_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, ".//button[@class='mat-icon-button mat-button-base']")))
        self.action.move_to_element(exit_btn)
        self.action.click(exit_btn)
        self.action.perform()

        print(f"{question}\n\t{reponse}")
        return {question.upper(): reponse}

    def close(self):
        self.driver.close()
