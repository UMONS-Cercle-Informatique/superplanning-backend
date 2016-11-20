from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.touch_actions import TouchActions

driver = webdriver.Firefox()
# Loading the hyper planning site
driver.get("https://hplanning2016.umons.ac.be/invite")

# We wait to be sure that the entire page is loaded.
# Without that, Selenium does not find the IDs.
try:
    dropDown = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "GInterface.Instances[1].Instances[1].bouton")))

    # Once the drop down menu is found, we click on it.
    dropDown.click()

    # We must wait that the page loads the sections
    section = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "GInterface.Instances[1].Instances[1]_19")))
    section.click()
finally:
    driver.close()
