import os
import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import sys
import time

# Thêm đường dẫn định nghĩa new_customer_page
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pages')))

from new_customer_page import NewCustomerPage
from login_page import LoginPage

class NewCustomerTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.login_page = LoginPage(cls.driver)
        cls.login_page.open_page("https://www.demo.guru99.com/V4/")
        cls.login_page.enter_username("mngr596391")
        cls.login_page.enter_password("punybYz")
        cls.login_page.click_login()
        time.sleep(1)
        cls.new_customer_page = NewCustomerPage(cls.driver)
        cls.new_customer_page.open_page("addcustomerpage.php")
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
        self.driver.find_element(*self.new_customer_page.address_textbox).send_keys(Keys.TAB)
        error_message = self.new_customer_page.get_error_message(error_locator)
        self.assertEqual(error_message, expected_message)
    
    def field_not_allow_special_characters(self, enter_field_method, error_locator, expected_message):
        enter_field_method("<")
        self.driver.find_element(*self.new_customer_page.address_textbox).send_keys(Keys.TAB)
        error_message = self.new_customer_page.get_error_message(error_locator)
        self.assertIn(error_message, expected_message)
        
    def field_not_allow_characters(self, enter_field_method, error_locator, expected_message):
        enter_field_method("abc") 
        self.driver.find_element(*self.new_customer_page.address_textbox).send_keys(Keys.TAB)
        error_message = self.new_customer_page.get_error_message(error_locator)
        self.assertIn(error_message, expected_message)
    
    def field_not_allow_numbers(self, enter_field_method, error_locator, expected_message):
        enter_field_method("123") 
        self.driver.find_element(*self.new_customer_page.address_textbox).send_keys(Keys.TAB)
        error_message = self.new_customer_page.get_error_message(error_locator)
    
    def field_not_allow_space(self, enter_field_method, error_locator, expected_message):
        enter_field_method(" ")
        self.driver.find_element(*self.new_customer_page.address_textbox).send_keys(Keys.TAB)
        error_message = self.new_customer_page.get_error_message(error_locator)

    # Test for each field
    
    # TC 1: Customer Name không để trống
    def test_empty_customer_name(self):
        self.field_must_not_be_blank(self.new_customer_page.enter_cusname, self.new_customer_page.cusname_error, "Customer name must not be blank")
        
    # TC2: Customer Name không phải số
    def test_number_customer_name(self):
        self.field_not_allow_numbers(self.new_customer_page.enter_cusname, self.new_customer_page.cusname_error, "Numbers are not allowed")
        
    # TC3: Customer Name không chứa ký tự đặc biệt
    def test_special_character_customer_name(self):
        self.field_not_allow_special_characters(self.new_customer_page.enter_cusname, self.new_customer_page.cusname_error, "Special characters are not allowed")
        
    # TC4: First character can not have space
    def test_spaces_in_cusname(self):
        self.field_not_allow_space(self.new_customer_page.enter_cusname, self.new_customer_page.cusname_error, "First character can not have space")
        
    # TC5: Customer Name chỉ chấp nhận chữ cái
    def test_character_customer_name(self):
        self.new_customer_page.enter_cusname("nhan")
        
        message_style = self.driver.find_element(*self.new_customer_page.cusname_error).get_attribute("style")
        self.assertIn("hidden", message_style)
    
    # TC6: Address không thể trống
    def test_empty_address(self):
        self.field_must_not_be_blank(self.new_customer_page.enter_address, self.new_customer_page.address_error, "Address Field must not be blank")
    
    # TC7: Address ký tự đầu tiên không để khoản trắng
    def test_spaces_in_address(self):
        self.field_not_allow_space(self.new_customer_page.enter_address, self.new_customer_page.address_error, "First character can not have space")
    
    # TC8: Address không chứa ký tự đặc biệt
    def test_special_characters_in_address(self):
        self.field_not_allow_special_characters(self.new_customer_page.enter_address, self.new_customer_page.address_error, "Special characters are not allowed")
        
    # TC9: Address chấp nhận chữ cái và số
    def test_valid_address(self):
        self.new_customer_page.enter_address("nhan")
        message_style = self.driver.find_element(*self.new_customer_page.address_error).get_attribute("style")
        self.assertIn("hidden", message_style)
        
    # TC10: City không chứa ký tự đặc biệt
    def test_special_characters_in_city(self):
        self.field_not_allow_special_characters(self.new_customer_page.enter_city, self.new_customer_page.city_error, "Special characters are not allowed")
        
    # TC11: City không thể trống
    def test_empty_city(self):
        self.field_must_not_be_blank(self.new_customer_page.enter_city, self.new_customer_page.city_error, "City Field must not be blank")
    
    # TC12: City không chứa số
    def test_number_in_city(self):
        self.field_not_allow_numbers(self.new_customer_page.enter_city, self.new_customer_page.city_error, "Numbers are not allowed")
        
    # TC13: City ký tự đầu tiên không để khoản trắng
    def test_spaces_in_city(self):
        self.field_not_allow_space(self.new_customer_page.enter_city, self.new_customer_page.city_error, "First character can not have space")
        
    # TC14: City chỉ chấp nhận chữ cái
    def test_valid_city(self):
        self.new_customer_page.enter_city("Danang")
        
        time.sleep(1)
        message_style = self.driver.find_element(*self.new_customer_page.city_error).get_attribute("style")
        self.assertIn("hidden", message_style)
    
    # TC15: State không chứa ký tự đặc biệt
    def test_special_characters_in_state(self):
        self.field_not_allow_special_characters(self.new_customer_page.enter_state, self.new_customer_page.state_error, "Special characters are not allowed")
    
    # TC16: State không thể trống
    def test_empty_state(self):
        self.field_must_not_be_blank(self.new_customer_page.enter_state, self.new_customer_page.state_error, "State must not be blank")
        
    # TC17: State không chứa số
    def test_number_in_state(self):
        self.field_not_allow_numbers(self.new_customer_page.enter_state, self.new_customer_page.state_error, "Numbers are not allowed")
    
    # TC18: State ký tự đầu tiên không để khoản trắng
    def test_spaces_in_state(self):
        self.field_not_allow_space(self.new_customer_page.enter_state, self.new_customer_page.state_error, "First character can not have space")
        
    # TC19: State chỉ chấp nhận chữ cái
    def test_valid_state(self):
        self.new_customer_page.enter_state("VN")
        
        message_style = self.driver.find_element(*self.new_customer_page.state_error).get_attribute("style")
        self.assertIn("hidden", message_style)
        
    # TC20: Pin không chứa ký tự đặc biệt
    def test_special_characters_in_pin(self):
        self.field_not_allow_special_characters(self.new_customer_page.enter_pinno, self.new_customer_page.pinno_error, "Special characters are not allowed")
    
    # TC21: Pin không thể trống
    def test_empty_pin(self):
        self.field_must_not_be_blank(self.new_customer_page.enter_pinno, self.new_customer_page.pinno_error, "PIN Code must not be blank")
        
    # TC22: Pin không chứa chữ cái
    def test_characters_in_pin(self):
        self.field_not_allow_characters(self.new_customer_page.enter_pinno, self.new_customer_page.pinno_error, "Characters are not allowed")
    
    # TC23: Pin ký tự đầu tiên không được khoản trắng
    def test_spaces_in_pin(self):
        self.field_not_allow_space(self.new_customer_page.enter_pinno, self.new_customer_page.pinno_error, "First character can not have space")
        
    # TC24: Pin chỉ chấp nhận 6 số
    def test_valid_pin(self):
        self.new_customer_page.enter_pinno("123456")
        
        message_style = self.driver.find_element(*self.new_customer_page.pinno_error).get_attribute("style")
        self.assertIn("hidden", message_style)
        
    # TC25: PIN không được ít hơn 6 số
    def test_too_short_pin(self):
        self.new_customer_page.enter_pinno("12345")
        
        error_message = self.new_customer_page.get_error_message(self.new_customer_page.pinno_error)
        self.assertIn("PIN Code must have 6 Digits", error_message)
    
    # TC26: PIN không nhiều hơn 6 số
    def test_too_long_pin(self):
        self.new_customer_page.enter_pinno("1234567")
        
        pinno = self.new_customer_page.find_element(*self.new_customer_page.pinno_textbox).get_attribute("value")
        self.assertIn("123456", pinno)
        
    # TC27: Mobile Number không chứa ký tự đặc biệt
    def test_special_characters_in_mobile_number(self):
        self.field_not_allow_special_characters(self.new_customer_page.enter_phoneno, self.new_customer_page.phoneno_error, "Special characters are not allowed")
    
    # TC28: Mobile Number không thể trống
    def test_empty_mobile_number(self):
        self.field_must_not_be_blank(self.new_customer_page.enter_phoneno, self.new_customer_page.phoneno_error, "Mobile no must not be blank")
        
    # TC29: Mobile Number không chứa ký tự
    def test_characters_in_mobile_number(self):
        self.field_not_allow_characters(self.new_customer_page.enter_phoneno, self.new_customer_page.phoneno_error, "Characters are not allowed")
        
    # TC30: Mobile Number ký tự đầu tiên không để khoản trắng
    def test_spaces_in_mobile_number(self):
        self.field_not_allow_space(self.new_customer_page.enter_phoneno, self.new_customer_page.phoneno_error, "First character can not have space")
        
    # TC31: Mobile Number chỉ chấp nhận số
    def test_valid_mobile_number(self):
        self.new_customer_page.enter_phoneno("123456789")
        
        message_style = self.driver.find_element(*self.new_customer_page.phoneno_error).get_attribute("style")
        self.assertIn("hidden", message_style)
        
    # TC32: E-mail không để trống
    def test_empty_email(self):
        self.field_must_not_be_blank(self.new_customer_page.enter_mailid, self.new_customer_page.mailid_error, "Email-ID must not be blank")
        
    # TC33: E-mail ký tự đầu tiên không để khoản trắng
    def test_spaces_in_email(self):
        self.field_not_allow_space(self.new_customer_page.enter_mailid, self.new_customer_page.mailid_error, "First character can not have space")
        
    # TC34: E-mail không hợp lệ
    def test_invalid_email(self):
        self.new_customer_page.enter_mailid("1422s")
        
        error_message = self.new_customer_page.get_error_message(self.new_customer_page.mailid_error)
        self.assertIn("Email-ID is not valid", error_message)
        
    # TC35: E-mail hợp lệ
    def test_valid_email(self):
        self.new_customer_page.enter_mailid("1412a@gmail.com")
        
        message_style = self.driver.find_element(*self.new_customer_page.mailid_error).get_attribute("style")
        self.assertIn("hidden", message_style)
        
    # TC36: Password phải ẩn 
    def test_is_password_hidden(self):
        self.new_customer_page.enter_password("punybYz")
        
        password = self.driver.find_element(*self.new_customer_page.password_textbox)
        self.assertEqual(password.get_attribute("type"), "password")
        
    # TC37: Submit thành công
    def test_submit(self):
        self.new_customer_page.enter_cusname("nhan")
        self.new_customer_page.enter_dob("10/16/2003")
        self.new_customer_page.enter_address("To 2")
        self.new_customer_page.enter_city("DaNang")
        self.new_customer_page.enter_state("VN")
        self.new_customer_page.enter_pinno("123456")
        self.new_customer_page.enter_phoneno("111111111")
        self.new_customer_page.enter_mailid("1412a@gmail.com")
        self.new_customer_page.enter_password("punybYz")
        self.new_customer_page.click_submit()
        
        success_message = self.new_customer_page.get_error_message(self.new_customer_page.heading_successfully)
        self.assertIn("Successfully", success_message)
        
        self.driver.back()

        
    # TC38: Người dùng có thể Reset
    def test_reset(self):
        self.new_customer_page.enter_cusname("nhan")
        self.new_customer_page.enter_dob("10/16/2003")
        self.new_customer_page.enter_address("To 2")
        self.new_customer_page.enter_city("DaNang")
        self.new_customer_page.enter_state("VN")
        self.new_customer_page.enter_pinno("123456")
        self.new_customer_page.enter_phoneno("111111111")
        self.new_customer_page.enter_mailid("1412a@gmail.com")
        self.new_customer_page.enter_password("punybYz")
        self.new_customer_page.click_reset()
        
        cusname = self.driver.find_element(*self.new_customer_page.cusname_textbox)
        dob = self.driver.find_element(*self.new_customer_page.dob_textbox)
        address = self.driver.find_element(*self.new_customer_page.address_textbox)
        city = self.driver.find_element(*self.new_customer_page.city_textbox)
        state = self.driver.find_element(*self.new_customer_page.state_textbox)
        pinno = self.driver.find_element(*self.new_customer_page.pinno_textbox)
        phoneno = self.driver.find_element(*self.new_customer_page.phoneno_textbox)
        mailid = self.driver.find_element(*self.new_customer_page.mailid_textbox)
        password = self.driver.find_element(*self.new_customer_page.password_textbox)
        
        self.assertEqual(cusname.get_attribute("value"), "")
        self.assertEqual(dob.get_attribute("value"), "")
        self.assertEqual(address.get_attribute("value"), "")
        self.assertEqual(city.get_attribute("value"), "")
        self.assertEqual(state.get_attribute("value"), "")
        self.assertEqual(pinno.get_attribute("value"), "")
        self.assertEqual(phoneno.get_attribute("value"), "")
        self.assertEqual(mailid.get_attribute("value"), "")
        self.assertEqual(password.get_attribute("value"), "")
 
  
if __name__ == "__main__":
    unittest.main()
    
        
    
    
    
    
    
    
    
    
    
    
    
    