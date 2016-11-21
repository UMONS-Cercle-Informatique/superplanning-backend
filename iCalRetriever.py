from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.touch_actions import TouchActions
from time import sleep

driver = webdriver.Chrome()
driver.implicitly_wait(3)
# Loading the hyper planning site
driver.get("https://hplanning2016.umons.ac.be/invite?fd=1")

# We wait to be sure that the entire page is loaded.
# Without that, Selenium does not find the IDs.
try:
    for i in range(0, 245):
        # The drop down menu with the list of sections
        dropDown = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "GInterface.Instances[1].Instances[1].bouton")))
        # Once the drop down menu is found, we click on it.
        dropDown.click()

        # We must wait that the page loads the sections
        if i >= 10:
            down = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "jspArrowDown")))
            down.click()
        section = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "GInterface.Instances[1].Instances[1]_" + str(i))))

        # The name of the section
        name = section.text
        # We open the planning
        section.click()

        # sleep(2)

        # The iCal pop-up
        iCalButton = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'Image_IcalDownload')))
        iCalButton.click()

        # We retrieve the link
        link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "GInterface.Instances[1].Instances[10]_lien_permanent")))

        # We write the name of the section and the link to the iCal to the file
        print("--------- [" + str(i+1) + "/245]")
        print("Année : " + name)
        print("Link : " + link.get_attribute("value"))
        print("---------")

        # We close the pop-up
        close = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "GInterface.Instances[1].Instances[10]_btns_0")))
        close.click()

        # We wait for the pop-up to fully close
        WebDriverWait(driver, 10).until_not(EC.element_to_be_clickable((By.ID, "GInterface.Instances[1].Instances[10]_btns_0")))
finally:
    driver.close()
