import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import sys
sys.path.insert(1, 'D://Subject//Testing//testing_assignment//pages')
from login_page import LoginPage


@pytest.fixture()
def driver():
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.implicitly_wait(10)
    yield driver
    driver.close()
    driver.quit()
    
# TC1: User-ID và Password không được để trống
def test_invalid_username(driver):
    login_page = LoginPage(driver)
    login_page.open_page("https://www.demo.guru99.com/V4/")
    login_page.enter_username("")
    login_page.enter_password("")
    login_page.click_login()
    
    # Hiển thị lỗi
    error_message = driver.find_element(By.ID, "message18").text
    assert "Invalid username or password" in error_message

# TC2: Người dùng có thể đăng nhập bằng User-ID và Password hợp lệ
def test_login(driver):
    login_page = LoginPage(driver)
    login_page.open_page("https://www.demo.guru99.com/V4/")
    login_page.enter_username("mngr596396")
    login_page.enter_password("sYvEhus")
    login_page.click_login()
    time.sleep(1)

# TC3: Password phải ẩn
def test_validate_password_field(driver):
    login_page = LoginPage(driver)
    login_page.open_page("https://www.demo.guru99.com/V4/")
    password_input = driver.find_element(*login_page.password_textbox) 
    password_input.click()  
    password_input.send_keys("123") 
    time.sleep(1)

    # kiểm tra password field có ở dạng password không
    password_type = password_input.get_attribute("type")
    assert password_type == "password", f"Expected 'password', but got '{password_type}'"
    
# TC4: Người dùng có thể Reset đăng nhập
def test_reset_login(driver):
    login_page = LoginPage(driver)
    login_page.open_page("https://www.demo.guru99.com/V4/")
    login_page.enter_username("mngr596396")
    login_page.enter_password("sYvEhus")
    login_page.click_reset()
    time.sleep(1)
    
    # Check fields are cleared
    username_input = driver.find_element(*login_page.username_textbox)
    password_input = driver.find_element(*login_page.password_textbox)
    
    assert username_input.get_attribute("value") == ""
    assert password_input.get_attribute("value") == ""
    