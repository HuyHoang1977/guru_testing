import os
import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import sys
import time

# Thêm đường dẫn đến widthdraw_page
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pages')))

from logout_page import LogoutPage
from login_page import LoginPage

class LogoutTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.login_page = LoginPage(cls.driver)
        cls.login_page.open_page("https://www.demo.guru99.com/V4/")
        cls.login_page.enter_username("mngr596538")
        cls.login_page.enter_password("EgAqYga")
        cls.login_page.click_login()
        time.sleep(1)

        
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def get_alert_text(self):
        alert = WebDriverWait(self.driver, 10).until(EC.alert_is_present())
        alert_text = alert.text
        alert.accept()  # Đóng alert sau khi lấy thông báo
        return alert_text
    
    def test_logout(self):
        self.logout_page = LogoutPage(self.driver)
        self.logout_page.open_page("Logout.php")
        error_message = self.get_alert_text()
        self.assertIn("Succesfully Logged Out", error_message)
        time.sleep(1)
        
class LogoutTestCustomer(LogoutTest):
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

if __name__ == "__main__":
    unittest.main()
