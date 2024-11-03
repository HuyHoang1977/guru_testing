import pytest
import os
import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import sys
import time

# Thêm đường dẫn đến login_page
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pages')))
from login_page import LoginPage
from logout_page import LogoutPage

class LoginTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.login_page = LoginPage(cls.driver)
        time.sleep(1)
        cls.login_page.open_page("https://www.demo.guru99.com/V4/")
    
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def get_alert_text(self):
        try:
            # Kiểm tra nếu có alert
            time.sleep(2)
            self.driver.implicitly_wait(1)  # Thay vì WebDriverWait
            alert = self.driver.switch_to.alert
            alert_text = alert.text
            alert.accept()  # Đóng alert sau khi lấy thông báo
            return alert_text
        except Exception as e:
            print("Alert không xuất hiện:", e)
            self.driver.back()  # Quay lại trang trước
            time.sleep(1)  # Đợi một chút trước khi tải lại trang
            self.driver.refresh()  # Tải lại trang
            raise AssertionError("Alert not found")
            

    def field_must_not_be_blank(self, enter_field_method, error_locator, expected_message):
        enter_field_method("")
        self.driver.find_element(*self.login_page.password_textbox).send_keys(Keys.TAB)
        error_message = self.login_page.get_error_message(error_locator)
        self.assertEqual(error_message, expected_message)
    
    def field_not_allow_special_characters(self, enter_field_method, error_locator, expected_message):
        enter_field_method("<")
        self.driver.find_element(*self.login_page.password_textbox).send_keys(Keys.TAB)
        error_message = self.login_page.get_error_message(error_locator)
        self.assertIn(error_message, expected_message)
        
    def field_not_allow_characters(self, enter_field_method, error_locator, expected_message):
        enter_field_method("abc") 
        self.driver.find_element(*self.login_page.password_textbox).send_keys(Keys.TAB)
        error_message = self.login_page.get_error_message(error_locator)
        self.assertIn(error_message, expected_message)
        
    
        # TC2: Người dùng có thể đăng nhập bằng User-ID và Password hợp lệ
    def test_login(self):
        self.login_page.enter_username("mngr596396")
        self.login_page.enter_password("sYvEhus")
        self.login_page.click_login()
        
         # Verify successful login
        success_message = self.login_page.get_error_message(self.login_page.heading_successfully)
        self.assertIn("Welcome", success_message)
        
         # Logout steps
        self.logout_page = LogoutPage(self.driver)  # Create an instance of LogoutPage
        self.logout_page.open_page("Logout.php")
        
        # Verify successful logout
        error_message = self.get_alert_text()
        self.assertIn("Succesfully", error_message)
        
        
    # TC1: User-ID và Password không được để trống
    def test_account_and_password_must_not_be_blank(self):
        self.field_must_not_be_blank(self.login_page.enter_username, self.login_page.username_error, "User-ID must not be blank")
        self.field_must_not_be_blank(self.login_page.enter_password, self.login_page.password_error, "Password must not be blank")
        

    # TC3: Password phải ẩn
    def test_validate_password_field(self):
        self.login_page.enter_password("123")
        
        password = self.driver.find_element(*self.login_page.password_textbox)
        self.assertEqual(password.get_attribute("type"), "password")

       
        
    # TC4: Người dùng có thể Reset đăng nhập
    def test_reset_login(self):
        self.login_page.enter_username("mngr596396")
        self.login_page.enter_password("sYvEhus")
        self.login_page.click_reset()
        
        # Check fields are cleared
        self.assertEqual(self.login_page.find_element(*self.login_page.username_textbox).get_attribute("value"), "")
        self.assertEqual(self.login_page.find_element(*self.login_page.password_textbox).get_attribute("value"), "")
        
   
if __name__ == "__main__":
    unittest.main()