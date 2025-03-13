from selenium.webdriver.common.by import By
def CGU(driver, ACCOUNT, PASSWORD):
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