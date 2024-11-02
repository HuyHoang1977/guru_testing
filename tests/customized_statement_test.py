import os
import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import sys
import time

# Thêm đường dẫn đến customized_statement_page
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pages')))

from customized_statement_page import CustomizedStatementPage
from login_page import LoginPage

class CustomizedStatementTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.login_page = LoginPage(cls.driver)
        cls.login_page.open_page("https://www.demo.guru99.com/V4/")
        cls.login_page.enter_username("mngr596538")
        cls.login_page.enter_password("EgAqYga")
        cls.login_page.click_login()
        time.sleep(1)
        cls.customized_statement_page = CustomizedStatementPage(cls.driver)
        cls.customized_statement_page.open_page("CustomisedStatementInput.php")
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
        self.driver.find_element(*self.customized_statement_page.numtransaction_field).send_keys(Keys.TAB)
        error_message = self.customized_statement_page.get_error_message(error_locator)
        self.assertEqual(error_message, expected_message)
    
    def field_not_allow_special_characters(self, enter_field_method, error_locator, expected_message):
        enter_field_method("<")
        self.driver.find_element(*self.customized_statement_page.numtransaction_field).send_keys(Keys.TAB)
        error_message = self.customized_statement_page.get_error_message(error_locator)
        self.assertIn(error_message, expected_message)
        
    def field_not_allow_characters(self, enter_field_method, error_locator, expected_message):
        enter_field_method("abc") 
        self.driver.find_element(*self.customized_statement_page.numtransaction_field).send_keys(Keys.TAB)
        error_message = self.customized_statement_page.get_error_message(error_locator)
        self.assertIn(error_message, expected_message)

    # Kiểm thử cho các trường
    def test_account_must_not_be_blank(self):
        self.field_must_not_be_blank(self.customized_statement_page.enter_account,
                                      self.customized_statement_page.account_error,
                                      "Account Number must not be blank")
        
    def test_account_not_allow_special_characters(self):
        self.field_not_allow_special_characters(self.customized_statement_page.enter_account,
                                               self.customized_statement_page.account_error,
                                               "Special characters are not allowed")
    
    def test_account_not_allow_characters(self):
        self.field_not_allow_characters(self.customized_statement_page.enter_account,
                                        self.customized_statement_page.account_error,
                                        "Characters are not allowed")

    def test_fdate_must_not_be_blank(self):
        self.field_must_not_be_blank(self.customized_statement_page.enter_fdate,
                                      self.customized_statement_page.fdate_error,
                                      "From Date Field must not be blank")
        
    def test_tdate_must_not_be_blank(self):
        self.field_must_not_be_blank(self.customized_statement_page.enter_tdate,
                                      self.customized_statement_page.tdate_error,
                                      "To Date Field must not be blank")
        
    def test_amount_lower_must_not_be_blank(self):
        self.field_must_not_be_blank(self.customized_statement_page.enter_amount_lower,
                                      self.customized_statement_page.amount_lower_error,
                                      "Amount lower limit must not be blank")
        
    def test_amount_lower_not_allow_special_characters(self):
        self.field_not_allow_special_characters(self.customized_statement_page.enter_amount_lower,
                                               self.customized_statement_page.amount_lower_error,
                                               "Special characters are not allowed")
        
    def test_amount_lower_not_allow_characters(self):
        self.field_not_allow_characters(self.customized_statement_page.enter_amount_lower,
                                        self.customized_statement_page.amount_lower_error,
                                        "Characters are not allowed")
        
    def test_numtransaction_must_not_be_blank(self):
        self.field_must_not_be_blank(self.customized_statement_page.enter_numtransaction,
                                      self.customized_statement_page.numtransaction_error,
                                      "Number of Transaction must not be blank")
        
    def test_numtransaction_not_allow_special_characters(self):
        self.field_not_allow_special_characters(self.customized_statement_page.enter_numtransaction,
                                               self.customized_statement_page.numtransaction_error,
                                               "Special characters are not allowed")
        
    def test_numtransaction_not_allow_characters(self):
        self.field_not_allow_characters(self.customized_statement_page.enter_numtransaction,
                                        self.customized_statement_page.numtransaction_error,
                                        "Characters are not allowed")
        
    def test_random_invalid_values(self):
        self.customized_statement_page.enter_account("")
        self.customized_statement_page.enter_fdate("")
        self.customized_statement_page.enter_tdate("30/12/2021")
        self.customized_statement_page.enter_amount_lower("abc")
        self.customized_statement_page.enter_numtransaction("<")
        self.customized_statement_page.click_submit()  # Nhấn nút Submit
        error_message = self.get_alert_text()
        self.assertIn("Please fill all fields", error_message)
        
    def test_invalid_source_destination_accounts(self):
        self.customized_statement_page.enter_account("13949")
        self.customized_statement_page.enter_fdate("01/01/2021")
        self.customized_statement_page.enter_tdate("30/12/2021")
        self.customized_statement_page.enter_amount_lower("10")
        self.customized_statement_page.enter_numtransaction("10")
        self.customized_statement_page.click_submit()  # Nhấn nút Submit
        error_message = self.get_alert_text()
        self.assertIn("not exist", error_message)

    def test_fdate_greater_than_tdate(self):
        self.customized_statement_page.enter_account("139497")
        self.customized_statement_page.enter_fdate("01/12/2021")
        self.customized_statement_page.enter_tdate("30/1/2021")
        self.customized_statement_page.enter_amount_lower("10")
        self.customized_statement_page.enter_numtransaction("10")
        self.customized_statement_page.click_submit()  # Nhấn nút Submit
        error_message = self.get_alert_text()
        self.assertIn("From Date not greater than To Date", error_message)

    def test_source_account_not_associated_with_manager(self):
        self.customized_statement_page.enter_account("139495")
        self.customized_statement_page.enter_fdate("01/01/2021")
        self.customized_statement_page.enter_tdate("30/12/2021")
        self.customized_statement_page.enter_amount_lower("10")
        self.customized_statement_page.enter_numtransaction("10")
        self.customized_statement_page.click_submit()  # Nhấn nút Submit
        error_message = self.get_alert_text()
        self.assertIn("not authorize", error_message)
    
    def test_valid_value(self):
        self.customized_statement_page.enter_account("139498")
        self.customized_statement_page.enter_fdate("01/01/2021")
        self.customized_statement_page.enter_tdate("30/12/2021")
        self.customized_statement_page.enter_amount_lower("10")
        self.customized_statement_page.enter_numtransaction("10")
        self.customized_statement_page.click_submit()
        success_message = self.customized_statement_page.get_error_message(self.customized_statement_page.heading_successfully) 
        self.assertIn("details", success_message)
        
    def test_reset(self):
        self.customized_statement_page.enter_account("139498")
        self.customized_statement_page.enter_fdate("01/01/2021")
        self.customized_statement_page.enter_tdate("30/12/2021")
        self.customized_statement_page.enter_amount_lower("10")
        self.customized_statement_page.enter_numtransaction("10")
        self.customized_statement_page.click_reset()
        
        account = self.driver.find_element(*self.customized_statement_page.account_field)
        fdate = self.driver.find_element(*self.customized_statement_page.fdate_field)
        tdate = self.driver.find_element(*self.customized_statement_page.tdate_field)
        amount_lower = self.driver.find_element(*self.customized_statement_page.amount_lower_field)
        numtransaction = self.driver.find_element(*self.customized_statement_page.numtransaction_field)
        
        self.assertEqual(account.get_attribute("value"), "")
        self.assertEqual(fdate.get_attribute("value"), "")
        self.assertEqual(tdate.get_attribute("value"), "")
        self.assertEqual(amount_lower.get_attribute("value"), "")
        self.assertEqual(numtransaction.get_attribute("value"), "")
        
class CustomizedStatementTestCustomer(CustomizedStatementTest):
    @classmethod
    def setUpClass(cls):
        # Gọi lại phương thức của lớp cha để đảm bảo driver được khởi tạo
        super().setUpClass()
        
        # Đăng xuất và đăng nhập lại với thông tin mới
        cls.login_page.open_page("https://www.demo.guru99.com/V4/")  # Mở lại trang đăng nhập
        cls.login_page.enter_username("2928")  # Thay thế username
        cls.login_page.enter_password("12345")  # Thay thế password
        cls.login_page.click_login()  # Đăng nhập với thông tin mới
        time.sleep(1)  # Thời gian chờ sau khi đăng nhập
        cls.customized_statement_page = CustomizedStatementPage(cls.driver)
        cls.customized_statement_page.open_page("CustomisedStatementInput.php")

if __name__ == "__main__":
    unittest.main()
