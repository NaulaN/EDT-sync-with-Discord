from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime


class Scraping(object):
    driver = webdriver.Chrome()
    hours: str
    edt = {}

    def __init__(self, username, password):
        # Ouvre la page dans Chrome
        self.driver.get('https://ent.iut.univ-paris8.fr/edt/presentations.php')
        # Se connecter
        self.driver.find_element(By.ID, "username").send_keys(username)
        self.driver.find_element(By.ID, "password").send_keys(password)
        self.driver.find_element(By.NAME, "submit").click()

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

    def getEDT(self):
        """ Update l'emploie du temps """
        todayDate = self.getWhatDayWeek()

        # TODO Corrigé les elements qui manque present sur l'emploie du temps (Nom de div bizarre)
        # Click sur l'emploie du temps qui correspond au jour de la semaine
        for element in self.driver.find_element(By.ID, "quadrillage").find_elements(By.CSS_SELECTOR, f"[style^=top]"):
            allElementsCanFind = self.driver.find_elements(By.CLASS_NAME,"ligne.petit") + self.driver.find_elements(By.CLASS_NAME,"lignegrey") + self.driver.find_elements(By.CLASS_NAME,"plage.petit")
            # ((todayDate if todayDate not in [5,6] else 0)*20)+6.6667 => only use for B group
            if element.get_attribute("style").count(f"margin-left: {((todayDate if todayDate not in [5,6] else 0)*20)+6.6667}%") >= 1 and len(element.text) > 0:
                # Cherche a quel heure il correspond sur l'emploie du temps.
                for elementHeure in allElementsCanFind:
                    if abs(int(elementHeure.get_attribute("style").split(";")[0].replace("top: ","").replace("px","")) - int(element.get_attribute("style").split(';')[0].replace("top: ","").replace("px",""))) in [30, 10]:
                        print(elementHeure.find_element(By.CLASS_NAME,"fright").text)
                        self.writeCours(element, elementHeure)
                        break
                # TODO Enlever les prints une fois fini !
                print(self.edt)
                print(element.text + "\n")
            # Quand c'est classe entiere.
            elif element.get_attribute("style").count(f"margin-left: {todayDate if todayDate not in [5,6] else 0*20}%") >= 1 and len(element.text) > 0:
                for elementHeure in allElementsCanFind:
                    if element.text.split('\n')[2] not in ["Amphi ", "Amphi2 "]: break
                    if abs(int(elementHeure.get_attribute("style").split(";")[0].replace("top: ", "").replace("px", ""))-int(element.get_attribute("style").split(';')[0].replace("top: ", "").replace("px", ""))) in [30, 10]:
                        print(elementHeure.find_element(By.CLASS_NAME, "fright").text)
                        self.writeCours(element, elementHeure)
                        break
                # TODO Enlever les prints une fois fini !
                print(self.edt)
                print(element.text + "\n")
