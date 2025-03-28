from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import base64
from io import BytesIO
from PIL import Image
import os
import Login
import PPT
from pathlib import Path
import json
import subprocess
import moocs

def School_login(num: int):
    if num == 0:
        Login.CGU(driver, ACCOUNT, PASSWORD)
    elif num == 1:
        Login.CLU(driver, ACCOUNT, PASSWORD)

schoool_list = ["長庚大學", "致理科技大學"]
PROFILE_PATH = Path("dependence\Profile")
driver = webdriver.Edge()
driver.set_window_size(1900, 1080)
if PROFILE_PATH.exists() == False:
    terminal_print = "Initialization Setting:\nChoose your school"
    while True:
        os.system("cls")
        print(terminal_print)
        for n, name in enumerate(schoool_list):
            print(f"[{n}] {name}")
        SCHOOL_NUM = int(input("Enter number:"))
        if schoool_list[SCHOOL_NUM] in schoool_list:
            break
        os.system("cls")
        print("Error Please enter again")
        time.sleep(3)
    terminal_print =  terminal_print.split("\n")[0] + "\nEnter account and password"
    while True:
        os.system("cls")
        print(terminal_print)
        ACCOUNT = input("Account:")
        PASSWORD = input("Password:")
        try:
            School_login(SCHOOL_NUM)
            break
        except:
            os.system("cls")
            print("Wrong with account or password")
            time.sleep(3)
    content = f"{ACCOUNT}\n{PASSWORD}"
    netrc = "dependence\Login.netrc"
    with open(netrc, "w") as f:
        f.write(content)
    subprocess.run(r"dependence\gpg\gpg.exe --output dependence\Login.gpg --symmetric dependence\Login.netrc")
    Path("dependence\Login.netrc").unlink()
    profile = {"school_num": SCHOOL_NUM}
    profile_path = Path("dependence\Profile")
    with open(profile_path, 'w') as f:
        json.dump(profile, f)
    os.system("cls")
    print("Setup Complete\nPlease restart")
    time.sleep(3)
    exit()

with open(PROFILE_PATH, "r") as f:
    PROFILE = json.load(f)
    SCHOOL_NUM = PROFILE["school_num"]

gpg_output = subprocess.run(r"dependence\gpg\gpg.exe --decrypt dependence\Login.gpg", capture_output=True, text=True).stdout.strip()
ACCOUNT, PASSWORD = gpg_output.split("\n")

terminal_print = f"School:{schoool_list[SCHOOL_NUM]}"

School_login(SCHOOL_NUM)

driver.implicitly_wait(10)

moocs.Download_handout(driver)