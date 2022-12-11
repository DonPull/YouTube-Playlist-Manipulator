import os
import time
import zipfile

import requests as requests
import wget as wget
from selenium.webdriver.common.by import By


def install_latest_chromedriver():
    # delete already existing chromedriver and then install the latest one to ensure no version issues
    if os.path.exists("chromedriver.exe"):
        os.remove("chromedriver.exe")

    # get the latest chrome driver version number
    url = 'https://chromedriver.storage.googleapis.com/LATEST_RELEASE'
    response = requests.get(url)
    version_number = response.text

    # build the donwload url
    download_url = "https://chromedriver.storage.googleapis.com/" + version_number + "/chromedriver_win32.zip"

    # download the zip file using the url built above
    latest_driver_zip = wget.download(download_url, 'chromedriver.zip')

    # extract the zip file
    with zipfile.ZipFile(latest_driver_zip, 'r') as zip_ref:
        zip_ref.extractall(path="./")  # you can specify the destination folder path here
    # delete the zip file downloaded above
    os.remove(latest_driver_zip)


def execute_script(driver, script, number_of_sec_before_fail=20, time_before_execute_sec=0, throw_exception=True):
    time.sleep(time_before_execute_sec)
    if number_of_sec_before_fail <= 0:
        number_of_sec_before_fail = 1

    for i in range(number_of_sec_before_fail):
        try:
            # driver.execute_script(script="return " + script.replace(".click()", "")).send_keys()
            elements = driver.execute_script(script=script)
            return elements
        except:
            time.sleep(1)

    if throw_exception:
        raise Exception(f'Script: "{script}" is incorrect!')


def find_element(driver, by, script, number_of_sec_before_fail=25, time_before_execute_sec=0, throw_exception=True):
    time.sleep(time_before_execute_sec)
    if number_of_sec_before_fail <= 0:
        number_of_sec_before_fail = 1

    for i in range(number_of_sec_before_fail):
        try:
            # driver.execute_script(script="return " + script.replace(".click()", "")).send_keys()
            #elements = driver.execute_script(script=script)
            element = driver.find_element(by, script)
            return element
        except:
            time.sleep(1)

    if throw_exception:
        raise Exception(f'Script: "{script}" is incorrect!')


def find_elements(driver, by, script, number_of_sec_before_fail=25, time_before_execute_sec=0, throw_exception=True):
    time.sleep(time_before_execute_sec)
    if number_of_sec_before_fail <= 0:
        number_of_sec_before_fail = 1

    for i in range(number_of_sec_before_fail):
        try:
            # driver.execute_script(script="return " + script.replace(".click()", "")).send_keys()
            #elements = driver.execute_script(script=script)
            element = driver.find_elements(by, script)
            return element
        except:
            time.sleep(1)

    if throw_exception:
        raise Exception(f'Script: "{script}" is incorrect!')