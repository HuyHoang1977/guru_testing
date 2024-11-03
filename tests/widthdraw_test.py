import os
import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import sys
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pages')))

from widthdraw_page import WidthdrawPage
from login_page import LoginPage

class WidthdrawTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.login_page = LoginPage(cls.driver)
        cls.login_page.open_page("https://www.demo.guru99.com/V4/")
        cls.login_page.enter_username("mngr596538")
        cls.login_page.enter_password("EgAqYga")
        cls.login_page.click_login()
        time.sleep(1)
        cls.widthdraw_page = WidthdrawPage(cls.driver)
        cls.widthdraw_page.open_page("WithdrawalInput.php")
        time.sleep(1)
        
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def get_alert_text(self):
        alert = WebDriverWait(self.driver, 10).until(EC.alert_is_present())
        alert_text = alert.text
        alert.accept() 
        return alert_text

    def field_must_not_be_blank(self, enter_field_method, error_locator, expected_message):
        enter_field_method("")
        self.driver.find_element(*self.widthdraw_page.description_field).send_keys(Keys.TAB)
        error_message = self.widthdraw_page.get_error_message(error_locator)
        self.assertEqual(error_message, expected_message)
    
    def field_not_allow_special_characters(self, enter_field_method, error_locator, expected_message):
        enter_field_method("<")
        self.driver.find_element(*self.widthdraw_page.description_field).send_keys(Keys.TAB)
        error_message = self.widthdraw_page.get_error_message(error_locator)
        self.assertIn(error_message, expected_message)
        
    def field_not_allow_characters(self, enter_field_method, error_locator, expected_message):
        enter_field_method("abc") 
        self.driver.find_element(*self.widthdraw_page.description_field).send_keys(Keys.TAB)
        error_message = self.widthdraw_page.get_error_message(error_locator)
        self.assertIn(error_message, expected_message)
        
    def field_valid_value(self, enter_field_method, error_locator, expected_message):
        enter_field_method("10") 
        self.driver.find_element(*self.widthdraw_page.description_field).send_keys(Keys.TAB)
        error_message = self.widthdraw_page.get_error_message(error_locator)
        self.assertEqual(error_message, expected_message)

    # Kiểm thử cho các trường
    def test_account_must_not_be_blank(self):
        self.field_must_not_be_blank(self.widthdraw_page.enter_account,
                                      self.widthdraw_page.account_error,
                                      "Account Number must not be blank")
        
    def test_account_not_allow_special_characters(self):
        self.field_not_allow_special_characters(self.widthdraw_page.enter_account,
                                               self.widthdraw_page.account_error,
                                               "Special characters are not allowed")
    
    def test_account_not_allow_characters(self):
        self.field_not_allow_characters(self.widthdraw_page.enter_account,
                                        self.widthdraw_page.account_error,
                                        "Characters are not allowed")
        
    def test_account_valid_value(self):
        self.field_valid_value(self.widthdraw_page.enter_account,
                               self.widthdraw_page.account_error,
                               "")

    def test_amount_must_not_be_blank(self):
        self.field_must_not_be_blank(self.widthdraw_page.enter_amount,
                                      self.widthdraw_page.amount_error,
                                      "Amount field must not be blank")  
 
    def test_amount_not_allow_special_characters(self):
        self.field_not_allow_special_characters(self.widthdraw_page.enter_amount,
                                               self.widthdraw_page.amount_error,
                                               "Special characters are not allowed")
        
    def test_amount_not_allow_characters(self):
        self.field_not_allow_characters(self.widthdraw_page.enter_amount,
                                        self.widthdraw_page.amount_error,
                                        "Characters are not allowed")
        
    def test_amount_valid_value(self):
        self.field_valid_value(self.widthdraw_page.enter_amount,
                               self.widthdraw_page.amount_error,
                               "")

    def test_description_cannot_be_blank(self):
        self.field_must_not_be_blank(self.widthdraw_page.enter_description,
                                      self.widthdraw_page.description_error,
                                      "Description can not be blank")
    
    def test_description_valid_value(self):
        self.field_valid_value(self.widthdraw_page.enter_description,
                               self.widthdraw_page.description_error,
                               "")
        
    def test_random_invalid_values(self):
        self.widthdraw_page.enter_account("")
        self.widthdraw_page.enter_amount("abc")
        self.widthdraw_page.enter_description("<")
        self.widthdraw_page.click_submit()  
        error_message = self.get_alert_text()
        self.assertIn("Please fill all fields", error_message)
        
    def test_invalid_source_destination_accounts(self):
        self.widthdraw_page.enter_account("13949")
        self.widthdraw_page.enter_amount("500")
        self.widthdraw_page.enter_description("Test")
        self.widthdraw_page.click_submit()  
        error_message = self.get_alert_text()
        self.assertIn("not exist", error_message)

    def test_insufficient_balance(self):
        self.widthdraw_page.enter_account("139497")
        self.widthdraw_page.enter_amount("10000")  
        self.widthdraw_page.enter_description("Test")
        self.widthdraw_page.click_submit()  
        error_message = self.get_alert_text()
        self.assertIn("Account Balance Low", error_message)

    def test_source_account_not_associated_with_manager(self):
        self.widthdraw_page.enter_account("139495")
        self.widthdraw_page.enter_amount("10")
        self.widthdraw_page.enter_description("Test")
        self.widthdraw_page.click_submit()  
        error_message = self.get_alert_text()
        self.assertIn("not authorize to debit money", error_message)
    
    def test_valid_value(self):
        account = "139498"
        amount = "5"
        description = "Test"
        
        self.widthdraw_page.enter_account(account)
        self.widthdraw_page.enter_amount(amount)
        self.widthdraw_page.enter_description(description)
        self.widthdraw_page.click_submit()
        
        success_message = self.widthdraw_page.get_error_message(self.widthdraw_page.heading_successfully) 
        self.assertIn("details of Withdrawal", success_message)
        
        displayed_account = self.widthdraw_page.get_displayed_value("account")
        displayed_amount = self.widthdraw_page.get_displayed_value("amount")
        displayed_description = self.widthdraw_page.get_displayed_value("description")
        
        self.assertEqual(account, displayed_account, "value not found!")
        self.assertEqual(amount, displayed_amount, "value not found!")
        self.assertEqual(description, displayed_description, "value not found!")

        
    def test_reset(self):
        self.widthdraw_page.enter_account("139498")
        self.widthdraw_page.enter_amount("5")
        self.widthdraw_page.enter_description("Test")
        self.widthdraw_page.click_reset()
        
        account = self.driver.find_element(*self.widthdraw_page.account_field)
        amount = self.driver.find_element(*self.widthdraw_page.amount_field)
        description = self.driver.find_element(*self.widthdraw_page.description_field)
        
        self.assertEqual(account.get_attribute("value"), "")
        self.assertEqual(amount.get_attribute("value"), "")
        self.assertEqual(description.get_attribute("value"), "")

if __name__ == "__main__":
    unittest.main()
