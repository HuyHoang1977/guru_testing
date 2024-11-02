
import os
import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import sys
import time

# Thêm đường dẫn đến fund_transfer_page
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pages')))

from fund_transfer_page import FundTransferPage
from login_page import LoginPage

class FundTransferTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.login_page = LoginPage(cls.driver)
        cls.login_page.open_page("https://www.demo.guru99.com/V4/")
        cls.login_page.enter_username("mngr596538")
        cls.login_page.enter_password("EgAqYga")
        cls.login_page.click_login()
        time.sleep(1)
        cls.fund_transfer_page = FundTransferPage(cls.driver)
        cls.fund_transfer_page.open_page("FundTransInput.php")
        time.sleep(1)
        
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def get_alert_text(self):
        alert = WebDriverWait(self.driver, 10).until(EC.alert_is_present())
        alert_text = alert.text
        alert.accept()  # Đóng alert sau khi lấy thông báo
        return alert_text

    def field_must_not_be_blank(self, enter_field_method, error_locator, expected_message):
        enter_field_method("")
        self.driver.find_element(*self.fund_transfer_page.description_field).send_keys(Keys.TAB)
        error_message = self.fund_transfer_page.get_error_message(error_locator)
        self.assertEqual(error_message, expected_message)
    
    def field_not_allow_special_characters(self, enter_field_method, error_locator, expected_message):
        enter_field_method("<")
        self.driver.find_element(*self.fund_transfer_page.description_field).send_keys(Keys.TAB)
        error_message = self.fund_transfer_page.get_error_message(error_locator)
        self.assertEqual(error_message, expected_message)
        
    def field_not_allow_characters(self, enter_field_method, error_locator, expected_message):
        enter_field_method("abc") 
        self.driver.find_element(*self.fund_transfer_page.description_field).send_keys(Keys.TAB)
        error_message = self.fund_transfer_page.get_error_message(error_locator)
        self.assertEqual(error_message, expected_message)

    # Kiểm thử cho các trường
    def test_payers_account_must_not_be_blank(self):
        self.field_must_not_be_blank(self.fund_transfer_page.enter_payer_account,
                                      self.fund_transfer_page.payer_account_error,
                                      "Payers Account Number must not be blank")
        
    def test_payers_account_not_allow_special_characters(self):
        self.field_not_allow_special_characters(self.fund_transfer_page.enter_payer_account,
                                               self.fund_transfer_page.payer_account_error,
                                               "Special characters are not allowed")
    
    def test_payers_account_not_allow_characters(self):
        self.field_not_allow_characters(self.fund_transfer_page.enter_payer_account,
                                        self.fund_transfer_page.payer_account_error,
                                        "Characters are not allowed")

    def test_payees_account_must_not_be_blank(self):
        self.field_must_not_be_blank(self.fund_transfer_page.enter_payee_account,
                                      self.fund_transfer_page.payee_account_error,
                                      "Payees Account Number must not be blank")
        
    def test_payees_account_not_allow_special_characters(self):
        self.field_not_allow_special_characters(self.fund_transfer_page.enter_payee_account,
                                               self.fund_transfer_page.payee_account_error,
                                               "Special characters are not allowed")
        
    def test_payees_account_not_allow_characters(self):
        self.field_not_allow_characters(self.fund_transfer_page.enter_payee_account,
                                        self.fund_transfer_page.payee_account_error,
                                        "Characters are not allowed")

    def test_amount_must_not_be_blank(self):
        self.field_must_not_be_blank(self.fund_transfer_page.enter_amount,
                                      self.fund_transfer_page.amount_error,
                                      "Amount field must not be blank")  
 
    def test_amount_not_allow_special_characters(self):
        self.field_not_allow_special_characters(self.fund_transfer_page.enter_amount,
                                               self.fund_transfer_page.amount_error,
                                               "Special characters are not allowed")
        
    def test_amount_not_allow_characters(self):
        self.field_not_allow_characters(self.fund_transfer_page.enter_amount,
                                        self.fund_transfer_page.amount_error,
                                        "Characters are not allowed")

    def test_description_cannot_be_blank(self):
        self.field_must_not_be_blank(self.fund_transfer_page.enter_description,
                                      self.fund_transfer_page.description_error,
                                      "Description can not be blank")
        
    def test_random_invalid_values(self):
        self.fund_transfer_page.enter_payer_account("123456")
        self.fund_transfer_page.enter_payee_account("")
        self.fund_transfer_page.enter_amount("abc")
        self.fund_transfer_page.enter_description("<")
        self.fund_transfer_page.click_submit()  # Nhấn nút Submit
        error_message = self.get_alert_text()
        self.assertIn("Please fill all fields", error_message)
        
    def test_invalid_source_destination_accounts(self):
        self.fund_transfer_page.enter_payer_account("13949")
        self.fund_transfer_page.enter_payee_account("139497")
        self.fund_transfer_page.enter_amount("500")
        self.fund_transfer_page.enter_description("Test")
        self.fund_transfer_page.click_submit()  # Nhấn nút Submit
        error_message = self.get_alert_text()
        self.assertIn("not exist", error_message)

    def test_same_source_destination_accounts(self):
        valid_account = "123456"
        self.fund_transfer_page.enter_payer_account(valid_account)
        self.fund_transfer_page.enter_payee_account(valid_account)
        self.fund_transfer_page.enter_amount("500")
        self.fund_transfer_page.enter_description("Test")
        self.fund_transfer_page.click_submit()  # Nhấn nút Submit
        error_message = self.get_alert_text()
        self.assertIn("Must Not be Same", error_message)

    def test_insufficient_balance(self):
        self.fund_transfer_page.enter_payer_account("139497")
        self.fund_transfer_page.enter_payee_account("139498")
        self.fund_transfer_page.enter_amount("10000")  # Giả sử số tiền này vượt quá số dư
        self.fund_transfer_page.enter_description("Test")
        self.fund_transfer_page.click_submit()  # Nhấn nút Submit
        error_message = self.get_alert_text()
        self.assertIn("Account Balance low", error_message)

    def test_source_account_not_associated_with_manager(self):
        self.fund_transfer_page.enter_payer_account("139495")
        self.fund_transfer_page.enter_payee_account("139496")
        self.fund_transfer_page.enter_amount("10")
        self.fund_transfer_page.enter_description("Test")
        self.fund_transfer_page.click_submit()  # Nhấn nút Submit
        error_message = self.get_alert_text()
        self.assertIn("not authorize", error_message)
    
    def test_valid_fund_transfer(self):
        # Nhập các giá trị vào form
        payer_account = "139498"
        payee_account = "139497"
        amount = "5"
        description = "Test"
        
        self.fund_transfer_page.enter_payer_account(payer_account)
        self.fund_transfer_page.enter_payee_account(payee_account)
        self.fund_transfer_page.enter_amount(amount)
        self.fund_transfer_page.enter_description(description)
        self.fund_transfer_page.click_submit()
        
        # Kiểm tra thông báo thành công
        success_message = self.fund_transfer_page.get_error_message(self.fund_transfer_page.heading_successfully) 
        self.assertIn("Details", success_message)
        
        # Kiểm tra các giá trị đã nhập có hiển thị trên trang hay không
        displayed_payer_account = self.fund_transfer_page.get_displayed_value("payer_account")
        displayed_payee_account = self.fund_transfer_page.get_displayed_value("payee_account")
        displayed_amount = self.fund_transfer_page.get_displayed_value("amount")
        displayed_description = self.fund_transfer_page.get_displayed_value("description")
        
        # Kiểm tra các giá trị
        self.assertEqual(payer_account, displayed_payer_account, "value not found!")
        self.assertEqual(payee_account, displayed_payee_account, "value not found!")
        self.assertEqual(amount, displayed_amount, "value not found!")
        self.assertEqual(description, displayed_description, "value not found!")

        
    def test_reset(self):
        self.fund_transfer_page.enter_payer_account("139498")
        self.fund_transfer_page.enter_payee_account("139497")
        self.fund_transfer_page.enter_amount("5")
        self.fund_transfer_page.enter_description("Test")
        self.fund_transfer_page.click_reset()
        
        payer_account = self.driver.find_element(*self.fund_transfer_page.payer_account_field)
        payee_account = self.driver.find_element(*self.fund_transfer_page.payee_account_field)
        amount = self.driver.find_element(*self.fund_transfer_page.amount_field)
        description = self.driver.find_element(*self.fund_transfer_page.description_field)
        
        self.assertEqual(payer_account.get_attribute("value"), "")
        self.assertEqual(payee_account.get_attribute("value"), "")
        self.assertEqual(amount.get_attribute("value"), "")
        self.assertEqual(description.get_attribute("value"), "")
        
class FundTransferTestCustomer(FundTransferTest):
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
        cls.fund_transfer_page = FundTransferPage(cls.driver)
        cls.fund_transfer_page.open_page("customerfundinput.php")

if __name__ == "__main__":
    unittest.main()
