from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import base64
from io import BytesIO
from PIL import Image
import os
import PPT

ACCOUNT = ""
PASSWORD = ""
driver = webdriver.Edge()
URL = "https://ids.cgu.edu.tw/nidp/idff/sso?id=11&sid=0&option=credential&sid=0&target=https://el.cgu.edu.tw/login.php"
driver.get(URL)
driver.implicitly_wait(10)
account_form = driver.find_element(by=By.ID, value="exampleInputEmail1")
account_form.clear()
account_form.send_keys(ACCOUNT)
password_form = driver.find_element(By.ID, "exampleInputPassword1")
password_form.clear()
password_form.send_keys(PASSWORD)
driver.execute_script("imageSubmit()")
driver.implicitly_wait(10)
myCourse_form = driver.find_element(By.PARTIAL_LINK_TEXT, "我的課程")
myCourse_form.click()
driver.implicitly_wait(10)

def Get_course_names_and_course_elements():
    course_elements = [div_element.find_element(By.TAG_NAME, "a") for div_element in driver.find_elements(By.TAG_NAME, "div") if div_element.get_attribute("class")=="text-left"][1:]
    course_names = [element.get_attribute("text") for element in course_elements]
    return course_elements, course_names

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

    time.sleep(5)
    viewer_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "viewer"))
    )
    canva_elements = [element for element in viewer_element.find_elements(By.TAG_NAME, "div") if element.get_attribute("class")=="canvasWrapper"]
    canva_element = canva_elements[1]
    canvas_base64 = driver.execute_script("""
        var canvas = arguments[0].querySelector("canvas");
        return canvas.toDataURL("image/png");
    """, canva_element)


    canvas_bytes = base64.b64decode(canvas_base64.split(",")[1])
    image = Image.open(BytesIO(canvas_bytes))
    image.save("image.png")

    print("[0]Continue  [1]Leave")
    Again = int(input("Enter number:"))
    if Again:
        break
    driver.switch_to.parent_frame()
    driver.switch_to.frame("s_sysbar")
    driver.execute_script("goPersonal()")
    time.sleep(5)