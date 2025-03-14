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

def School_login(num: int):
    if num == 0:
        Login.CGU(driver, ACCOUNT, PASSWORD)

schoool_list = ["長庚大學"]
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
    profile = {"school_num": SCHOOL_NUM}
    profile_path = Path("dependence\Profile")
    with open(profile_path, 'w') as f:
        json.dump(profile, f)

with open(PROFILE_PATH, "r") as f:
    PROFILE = json.load(f)
    SCHOOL_NUM = PROFILE["school_num"]

gpg_output = subprocess.run(r"dependence\gpg\gpg.exe --decrypt dependence\Login.gpg", capture_output=True, text=True).stdout.strip()
ACCOUNT, PASSWORD = gpg_output.split("\n")

terminal_print = f"School:{schoool_list[SCHOOL_NUM]}"

School_login(SCHOOL_NUM)

driver.implicitly_wait(10)

def Wait_exists(id: str=None, name:str=None, frame=None):
    while True:
        if id != None:
            element_exists = driver.execute_script(f"return document.getElementById('{id}') !== null;")
        else:
            element_exists = driver.execute_script(f"return document.getElementsByName('{name}').length > 0;")
        if element_exists == True:
            if frame != None:
                driver.switch_to.frame(frame)
            break
        time.sleep(2)


def Get_course_names_and_course_elements():
    course_elements = [div_element.find_element(By.TAG_NAME, "a") for div_element in driver.find_elements(By.TAG_NAME, "div") if div_element.get_attribute("class")=="text-left"][1:]
    course_names = [element.get_attribute("text") for element in course_elements]
    return course_elements, course_names

def Get_chapters():
    driver.switch_to.parent_frame()
    Wait_exists(name="s_catalog")
    driver.switch_to.frame("s_catalog")
    wait = WebDriverWait(driver, 10)
    iframe = wait.until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
    Wait_exists("pathtree", frame=iframe)
    chapter_elements = []
    chapter_names = []
    for span_element in driver.find_elements(By.TAG_NAME, "span"):
        try:
            if span_element.find_element(By.TAG_NAME, "div").get_attribute("class") != None:
                a_element = span_element.find_element(By.TAG_NAME, "a")
                chapter_elements.append(a_element)
                chapter_names.append(a_element.get_attribute("text"))
        except:
            continue
    return chapter_names, chapter_elements

while True:
    driver.switch_to.parent_frame()
    driver.switch_to.frame("s_main")
    course_elements, course_names = Get_course_names_and_course_elements()
    time.sleep(2)
    try:
        os.system("cls")
        for n, name in enumerate(course_names):
            print(f"[{n}]{name}", end='  ')
        print()
        choose_course_index = int(input("Enter number:"))
        course_elements[choose_course_index].click()
    except:
        continue
    driver.implicitly_wait(10)
    time.sleep(5)

    chapter_names, chapter_elements = Get_chapters()
    for n, name in enumerate(chapter_names):
        print(f"[{n}]{name}", end='  ')
    print()
    choose_chapter_index = int(input("Enter number:"))
    chapter_elements[choose_chapter_index].click()

    time.sleep(5)
    driver.switch_to.default_content()
    driver.switch_to.frame("s_main")
    Wait_exists("viewer")
    viewer_element = driver.find_element(By.ID, "viewer")
    

    next_button = driver.find_element(By.ID, "next")
    total_page = int(driver.find_element(By.ID, "pageNumber").get_attribute("max"))
    images = []
    n = 1
    loop = True
    for n in range(1, total_page+1):
        for element in viewer_element.find_elements(By.TAG_NAME, "div"):
            if element.get_attribute("class")=="page" and element.get_attribute("data-page-number")==str(n):
                Wait_exists(f"page{n}")
                canva_element = element.find_element(By.TAG_NAME, "div")
        # canva_element = [element for element in viewer_element.find_elements(By.TAG_NAME, "div") if element.get_attribute("class")=="page" and element.get_attribute("data-page-number")==str(n)][0].find_element(By.TAG_NAME, "div")
        
        canvas_base64 = driver.execute_script("""
            var canvas = arguments[0].querySelector("canvas");
            return canvas.toDataURL("image/png");
        """, canva_element)


        canvas_bytes = base64.b64decode(canvas_base64.split(",")[1])
        image = Image.open(BytesIO(canvas_bytes))
        save_path = f"output\image\{n}.png"
        image.save(save_path)
        images.append(save_path)
        if n != total_page:
            next_button.click()
            driver.implicitly_wait(10)
            time.sleep(2)
    img_width, img_height = image.size
    canva_scale = float(f"{img_width/img_height:.1f}")
    # print(canva_scale)
    base_size = 13.33
    if canva_scale >= 1:
        canva_size = (base_size, base_size / canva_scale)
    elif canva_scale <= 1:
        canva_size = (base_size * canva_scale, base_size)
    pptx = PPT.createPPT(images, canva_size)
    pptx.save(f"output\{chapter_names[choose_chapter_index]}.pptx")
    for image in Path("output\image").iterdir():
        image.unlink()

    print("[0]Continue  [1]Leave")
    Again = int(input("Enter number:"))
    if Again:
        break
    driver.switch_to.parent_frame()
    driver.switch_to.frame("s_sysbar")
    driver.execute_script("goPersonal()")
    time.sleep(5)