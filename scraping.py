from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime


class Scraping(object):
    driver = webdriver.Chrome()
    hours: str
    edt = {}

    def __init__(self, username, password):
        # Ouvre la page dans Chrome
        self.driver.delete_all_cookies()
        self.driver.get('https://ent.iut.univ-paris8.fr/edt/presentations.php')
        # Se connecter
        self.driver.find_element(By.ID, "username").send_keys(username)
        self.driver.find_element(By.ID, "password").send_keys(password)
        self.driver.find_element(By.NAME, "submit").click()
        self.getEDT()

    def getWhatDayWeek(self) -> int:
        """ Récupère de 0..7, le jours de la semaine. """
        return datetime.today().weekday()

    def writeCours(self, element, elementHeure):
        """ Écrit l'heure en index et crée une liste contenant les infos concernant le cours """
        hoursIndex = elementHeure.find_element(By.CLASS_NAME,"fright").text.split("h")
        hoursIndex = float(f"{hoursIndex[0]}.{hoursIndex[1]}") if len(hoursIndex) == 2 else int(hoursIndex[0])
        self.edt[hoursIndex] = []
        for n,el in enumerate(element.text.split("\n")):
            self.edt[hoursIndex].append(el)

    def getEDT(self, todayDate=int(datetime.today().weekday())):
        """ Update l'emploie du temps """
        # Click sur l'emploie du temps qui correspond au jour de la semaine
        for element in self.driver.find_elements(By.CLASS_NAME, f"jours.jour{todayDate+1}.plageDIVn"):
            if len(element.text) > 0:
                allElementsCanFind = self.driver.find_elements(By.CLASS_NAME,"ligne.petit") + self.driver.find_elements(By.CLASS_NAME,"lignegrey") + self.driver.find_elements(By.CLASS_NAME,"plage.petit")                # ((todayDate if todayDate not in [5,6] else 0)*20)+6.6667 => only use for B group
                print(element.get_attribute("style"))
                print(element.text)
                if element.text.count("Amphi") >= 1 or element.text.count("Amphi2") >= 1:
                    for elementHeure in allElementsCanFind:
                        if abs(int(elementHeure.get_attribute("style").split(";")[0].replace("top: ", "").replace("px", ""))-int(element.get_attribute("style").split(';')[0].replace("top: ", "").replace("px", ""))) in [30, 10]:
                            print(elementHeure.text)
                            self.writeCours(element, elementHeure)
                            break
                else:
                    for style in element.get_attribute("style").split(";"):
                        print(style)
                        print(style.count(f" margin-left: {((todayDate+1 if todayDate not in [5,6] else 0)*10)+3.3333}"))
                        if style.count(f" margin-left: {((todayDate+1 if todayDate not in [5,6] else 0)*10)+3.3333}") >= 1:
                            for elementHeure in allElementsCanFind:
                                print(abs(int(elementHeure.get_attribute("style").split(";")[0].replace("top: ","").replace("px","")) - int(element.get_attribute("style").split(';')[0].replace("top: ","").replace("px",""))))
                                if abs(int(elementHeure.get_attribute("style").split(";")[0].replace("top: ","").replace("px","")) - int(element.get_attribute("style").split(';')[0].replace("top: ","").replace("px",""))) in [30,10]:
                                    print(elementHeure.text)
                                    self.writeCours(element, elementHeure)
                                    break
        print(self.edt)
