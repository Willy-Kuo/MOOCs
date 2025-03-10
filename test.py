from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time

ACCOUNT = "b1228048"
PASSWORD = "52710731"
driver = webdriver.Edge()
driver.set_window_size(1920, 1200)
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

def Get_course_list():
    course_class = driver.find_element(By.NAME, "s_sys")
    print(course_class[0])
# Get_course_list()
driver.switch_to.frame("s_main")
course_elements_list = [div_element.find_element(By.TAG_NAME, "a") for div_element in driver.find_elements(By.TAG_NAME, "div") if div_element.get_attribute("class")=="text-left"][1:]  #TAG a
course_name_list = [element.get_attribute("text") for element in course_elements_list]
course_elements_list[2].click()

time.sleep(3)
# print([element.get_attribute("class") for element in driver.find_elements(By.TAG_NAME, "div")])
viewer_element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "viewer"))
)
graphic_elements = [element for element in viewer_element.find_elements(By.TAG_NAME, "div") if element.get_attribute("class")=="canvasWrapper"]
print(graphic_elements)
graphic_elements[2].screenshot("image.png")
driver.save_screenshot("full_screenshot.png")
driver.quit()