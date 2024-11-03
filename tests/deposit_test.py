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
from deposit_page import DepositPage

class DepositTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.login_page = LoginPage(cls.driver)
        cls.login_page.open_page("https://www.demo.guru99.com/V4/")
        cls.login_page.enter_username("mngr596391")
        cls.login_page.enter_password("punybYz")
        cls.login_page.click_login()
        time.sleep(1)
        cls.deposit_page = DepositPage(cls.driver)
        cls.deposit_page.open_page("DepositInput.php")
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
        self.driver.find_element(*self.deposit_page.amount_textbox).send_keys(Keys.TAB)
        error_message = self.deposit_page.get_error_message(error_locator)
        self.assertEqual(error_message, expected_message)
    
    def field_not_allow_special_characters(self, enter_field_method, error_locator, expected_message):
        enter_field_method("<")
        self.driver.find_element(*self.deposit_page.amount_textbox).send_keys(Keys.TAB)
        error_message = self.deposit_page.get_error_message(error_locator)
        self.assertIn(error_message, expected_message)
        
    def field_not_allow_characters(self, enter_field_method, error_locator, expected_message):
        enter_field_method("abc") 
        self.driver.find_element(*self.deposit_page.amount_textbox).send_keys(Keys.TAB)
        error_message = self.deposit_page.get_error_message(error_locator)
        self.assertIn(error_message, expected_message)
    
    def field_not_allow_space_characters(self, enter_field_method, error_locator, expected_message):
        enter_field_method(" ")
        self.driver.find_element(*self.deposit_page.amount_textbox).send_keys(Keys.TAB)
        error_message = self.deposit_page.get_error_message(error_locator)
        self.assertIn(error_message, expected_message)
        
    # TC1: Account No không để trống
    def test_empty_account_no(self):
        self.field_must_not_be_blank(
            self.deposit_page.enter_accountno, 
            self.deposit_page.accountno_error, 
            "Account Number must not be blank")
        
    # TC2: "Account No" không có kí tự chữ
    def test_characters_in_account_no(self):
        self.field_not_allow_characters(
            self.deposit_page.enter_accountno, 
            self.deposit_page.accountno_error, 
            "Characters are not allowed")
        
    # TC3: "Account No" không có kí tự đặc biệt
    def test_special_characters_in_account_no(self):
        self.field_not_allow_special_characters(
            self.deposit_page.enter_accountno, 
            self.deposit_page.accountno_error,
            "Special characters are not allowed")
        
    # TC4: "Account No" hợp lệ
    def test_valid_account_no(self):
        self.deposit_page.enter_accountno("139408")
        
        message_style = self.driver.find_element(*self.deposit_page.accountno_error).get_attribute("style")
        self.assertIn("hidden", message_style)
        
    # TC5: Amount không để trống
    def test_empty_amount(self):
        self.field_must_not_be_blank(
            self.deposit_page.enter_amount, 
            self.deposit_page.amount_error, 
            "Amount field must not be blank")
    
    # TC 6: "Amount" không có kí tự chữ
    def test_characters_in_amount(self):
        self.field_not_allow_characters(
            self.deposit_page.enter_amount, 
            self.deposit_page.amount_error, 
            "Characters are not allowed")
        
    # TC 7: "Amount" không có kí tự đặc biệt
    def test_special_characters_in_amount(self):
        self.field_not_allow_special_characters(
            self.deposit_page.enter_amount, 
            self.deposit_page.amount_error,
            "Special characters are not allowed")
        
    # TC 8: "Amount" hợp lệ
    def test_valid_amount(self):
        self.deposit_page.enter_amount("10")
        
        message_style = self.driver.find_element(*self.deposit_page.amount_error).get_attribute("style")
        self.assertIn("hidden", message_style)
        
    # TC 9: Description không để trống
    def test_empty_description(self):
        self.field_must_not_be_blank(
            self.deposit_page.enter_description, 
            self.deposit_page.description_error, 
            "Description can not be blank")
        
    # TC 10: Submit thành công
    def test_submit_success(self):
        self.deposit_page.enter_accountno("139408")
        self.deposit_page.enter_amount("10")
        self.deposit_page.enter_description("Test")
        self.deposit_page.click_submit()
        
        message = self.get_alert_text()
        self.assertIn("Successfully", message)
        
        self.driver.back()
        
    # TC 11: Người dùng có thể Reset
    def test_reset(self):
        self.deposit_page.enter_accountno("139408")
        self.deposit_page.enter_amount("10")
        self.deposit_page.enter_description("Test")
        self.deposit_page.click_reset()
        
        account = self.driver.find_element(*self.deposit_page.accountno_textbox)
        amount = self.driver.find_element(*self.deposit_page.amount_textbox)
        description = self.driver.find_element(*self.deposit_page.description_textbox)
        
        self.assertEqual(account.get_attribute("value"), "")
        self.assertEqual(amount.get_attribute("value"), "")
        self.assertEqual(description.get_attribute("value"), "")

    
        
    
        