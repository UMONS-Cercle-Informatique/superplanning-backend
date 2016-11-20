from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.touch_actions import TouchActions

driver = webdriver.Chrome()
# Loading the hyper planning site
driver.get("https://hplanning2016.umons.ac.be/invite")

try:
    f = open("links", "w")

    # We wait to be sure that the entire page is loaded.
    # Without that, Selenium does not find the IDs.
    try:
        # The drop down menu with the list of sections
        dropDown = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "GInterface.Instances[1].Instances[1].bouton")))

        for i in range(0, 245):
            # Once the drop down menu is found, we click on it.
            dropDown.click()

            # We must wait that the page loads the sections
            section = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "GInterface.Instances[1].Instances[1]_" + str(i))))

            # The name of the section
            name = section.text

            # We open the planning
            section.click()

            # The iCal pop-up
            iCalButton = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="id_33"]/table/tbody/tr/td[6]/div')))

            iCalButton.click()

            link = driver.find_element_by_id("GInterface.Instances[1].Instances[10]_lien_permanent")
            f.write(name + " " + link.get_attribute("value") + '\n')

            close = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "GInterface.Instances[1].Instances[10]_btns_0")))
            close.click()
    finally:
        driver.close()

finally:
    f.close()
