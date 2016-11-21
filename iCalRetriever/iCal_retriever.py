# -*- coding: utf-8 -*-
""" This module is used to retrieve the iCal links from the hypperplanning website.
    It relies on Selenium to load and interact with the website.

    Every function tries 4 times to perform the action. If it fails, the script stops with a specific exit code.

    Author: Gaëtan Staquet
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.touch_actions import TouchActions
from selenium.common.exceptions import WebDriverException
from sys import exit
from time import sleep
import csv

def click_drop_down(driver):
    """ Opens the drop down menu that allows the user to select a section.
        The menu must be accessible (which means that every pop-up window must be closed before calling this function).
    """
    attempts = 0

    while attempts <= 3:
        try:
            dropDown = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "GInterface.Instances[1].Instances[1].bouton")))
            dropDown.click()
            return
        except WebDriverException:
            attempts += 1
    print("Unable to open the drop down menu. Please relaunch this script.")
    exit(1)

def scroll_down(driver):
    """ Once the drop down menu is opened, we can scroll down to access more sections. If we don't scroll, the elements are not visible and futhermore are not clickable.
        The drop down menu must be opened before calling this function.
    """
    attempts = 0

    while attempts <= 3:
        try:
            down = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "jspArrowDown")))
            down.click()
            return
        except WebDriverException:
            attempts += 1
    print("Unable to scroll the drop down menu. Please relaunch this script.")
    exit(2)

def click_section(driver, number):
    """ To open the planning (and to be able to retrieve the iCal link), we must click on the desired section.
    Args:
        number (int): the number of the section to load (must be between 0 and 244 included).

    Returns:
        string: the name of the selected section.
    """
    attempts = 0

    while attempts <= 3:
        try:
            section = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "GInterface.Instances[1].Instances[1]_" + str(number))))
            name = section.text
            section.click()
            return name
        except WebDriverException:
            attempts += 1
    print("Unable to select the section " + str(i) + " in the list. Please relaunch this script.")
    exit(3)

def open_iCal_window(driver):
    """ Once a section is loaded, we must open the iCal window.
        The correct section must be clicked before calling this function.
    """
    attempts = 0

    while attempts <= 3:
        try:
            iCalButton = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'Image_IcalDownload')))
            iCalButton.click()
            return
        except WebDriverException:
            attempts += 1
    print("Unable to open the iCal window. Please relaunch this script.")
    exit(4)

def retrieve_link(driver):
    """ Once the iCal window is opened, we can retrieve the link to the iCal file.
        The iCal window must be opened before calling this function.

        Returns:
            string: the link to the iCal file.
    """
    attempts = 0

    while attempts <= 3:
        try:
            link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "GInterface.Instances[1].Instances[10]_lien_permanent")))
            return link.get_attribute("value")
        except WebDriverException:
            attempts += 1
    print("Unable to retrieve the iCal link. Please relaunch this script.")
    exit(5)

def close_iCall_window(driver):
    """ Once the iCal link is retrieved, the iCal window can be closed.
        This function also waits for the window to be fully closed.
        The iCal window must be opened before calling this function.
    """
    attempts = 0

    while attempts <= 3:
        try:
            close = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "GInterface.Instances[1].Instances[10]_btns_0")))
            close.click()
            WebDriverWait(driver, 10).until_not(EC.element_to_be_clickable((By.ID, "GInterface.Instances[1].Instances[10]_btns_0")))
            return
        except WebDriverException:
            attempts += 1
    print("Unable to close the iCal window. Please relaunch this script.")
    exit(6)

#driver = webdriver.Chrome()
# or
driver = webdriver.Firefox()

# Loading the hyper planning site.
driver.get("https://hplanning2016.umons.ac.be/invite?fd=1")

try:
    # Do not forget to change the years!
    fi = open("2016-2017 - links icalendar", "w")
    try:
        for i in xrange(0, 245):
            # We open the drop down menu.
            click_drop_down(driver)

            # We wait to be sure that everything is fully loaded.
            sleep(1)

            # To be sure that the element we want to reach is visible, we scroll down the drop down menu.
            # We can't do it immediately because the first elements would become unclickable.
            if i >= 3:
                scroll_down(driver)

            # We can click the section we want and retrieve the name of this section.
            name = click_section(driver, i)
            
            # We wait to be sure that everything is fully loaded.
            sleep(5)

            # We open the iCal window.
            open_iCal_window(driver)

            # We retrieve the link from that window.
            link = retrieve_link(driver)

            # We write the name of the section and the link to the iCal to the file.
            # We also write in the console to be able to know what section the script has already reached.
            print("--------- [" + str(i) + "/244]")
            print("Année : " + name)
            print("Link : " + link)
            print("---------")
            fi.write("--------- [" + str(i) + "/244]\n")
            fi.write("Année : " + name + '\n')
            fi.write("Link : " + link + '\n')
            fi.write("---------\n")

            # We close the pop-up.
            close_iCall_window(driver)

            sleep(1)
    finally:
        driver.close()
finally:
    fi.close()
