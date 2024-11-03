import os
import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import sys
import time

# Thêm đường dẫn đến new_account_page
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pages')))
from new_account_page import NewAccountPage
from login_page import LoginPage
from logout_page import LogoutPage

class NewAccountTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.login_page = LoginPage(cls.driver)
        cls.login_page.open_page("https://www.demo.guru99.com/V4/")
        cls.login_page.enter_username("mngr596391")
        cls.login_page.enter_password("punybYz")
        cls.login_page.click_login()
        time.sleep(1)
        cls.new_account_page = NewAccountPage(cls.driver)
        cls.new_account_page.open_page("addAccount.php")
        time.sleep(1)
        
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
        self.driver.find_element(*self.new_account_page.initial_deposit_textbox).send_keys(Keys.TAB)
        error_message = self.new_account_page.get_error_message(error_locator)
        self.assertEqual(error_message, expected_message)
    
    def field_not_allow_special_characters(self, enter_field_method, error_locator, expected_message):
        enter_field_method("<")
        self.driver.find_element(*self.new_account_page.initial_deposit_textbox).send_keys(Keys.TAB)
        error_message = self.new_account_page.get_error_message(error_locator)
        self.assertIn(error_message, expected_message)
        
    def field_not_allow_characters(self, enter_field_method, error_locator, expected_message):
        enter_field_method("abc") 
        self.driver.find_element(*self.new_account_page.initial_deposit_textbox).send_keys(Keys.TAB)
        error_message = self.new_account_page.get_error_message(error_locator)
        self.assertIn(error_message, expected_message)
    
    def field_not_allow_space_characters(self, enter_field_method, error_locator, expected_message):
        enter_field_method(" ")
        self.driver.find_element(*self.new_account_page.initial_deposit_textbox).send_keys(Keys.TAB)
        error_message = self.new_account_page.get_error_message(error_locator)
        self.assertIn(error_message, expected_message)
        

    # TC1: Customer ID không để trống
    def test_invalid_customer_id(self):
        self.field_must_not_be_blank(self.new_account_page.enter_customer_id, self.new_account_page.account_id_error, "Customer ID is required")

    # TC2: "Customer ID" không có kí tự chữ
    def test_characters_in_cusid(self):
        self.field_not_allow_characters(self.new_account_page.enter_customer_id, self.new_account_page.account_id_error, "Characters are not allowed")

    # TC3: "Customer ID" có kí tự đặc biệt
    def test_special_characters_in_cusid(self):
        self.field_not_allow_special_characters(self.new_account_page.enter_customer_id, self.new_account_page.account_id_error, "Special characters are not allowed")

    # TC4: "Customer ID" kí tự đầu không được là khoảng trắng
    def test_space_in_cusid(self):
        self.field_not_allow_space_characters(self.new_account_page.enter_customer_id, self.new_account_page.account_id_error, "First character can not have space")

    # TC5: "Customer ID" hợp lệ
    def test_valid_cusid(self):
        self.new_account_page.enter_customer_id("57747")
        
        # Check error message
        time.sleep(1)
        message_style = self.driver.find_element(*self.new_account_page.account_id_error).get_attribute("style")
        self.assertIn("hidden", message_style)
        
    # TC6: Submit thành công   
    def test_submit(self):
        self.new_account_page.enter_customer_id("57747")
        self.new_account_page.enter_initial_deposit("1234567")
        self.new_account_page.click_submit()
        
        success_message = self.new_account_page.get_error_message(self.new_account_page.heading_successfully)
        self.assertIn("Successfully", success_message)
        
        self.driver.back()
        
    # TC7: Người dùng có thể Reset
    def test_reset(self):
        self.new_account_page.enter_customer_id("57747")
        self.new_account_page.enter_initial_deposit("1234567")
        self.new_account_page.click_reset()
        
        # Check fields are cleared
        cusid_input = self.driver.find_element(*self.new_account_page.customer_id_textbox)
        deposit_input = self.driver.find_element(*self.new_account_page.initial_deposit_textbox)
        account_type_input = self.driver.find_element(*self.new_account_page.account_type_combobox)
        
        assert cusid_input.get_attribute("value") == ""
        assert deposit_input.get_attribute("value") == ""
        assert account_type_input.get_attribute("value") == "Savings"

if __name__ == "__main__":
    unittest.main()
    