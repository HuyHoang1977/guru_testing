from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class NewCustomerPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        
        # Locators
        self.cusname_textbox = (By.NAME, "name")
        self.dob_textbox = (By.NAME, "dob")
        self.address_textbox = (By.NAME, "addr")
        self.city_textbox = (By.NAME, "city")
        self.state_textbox = (By.NAME, "state")
        self.pinno_textbox = (By.NAME, "pinno")
        self.phoneno_textbox = (By.NAME, "telephoneno")
        self.mailid_textbox = (By.NAME, "emailid")
        self.password_textbox = (By.NAME, "password")
        
        self.submit_button = (By.XPATH, "//input[@value='Submit']")
        self.reset_button = (By.XPATH, "//input[@value='Reset']")
        
        # Locators for error messages (these IDs may vary depending on actual implementation)
        self.heading_successfully = (By.CLASS_NAME, "heading3")
        self.cusname_error = (By.ID, "message")
        self.dob_error = (By.ID, "message24")
        self.address_error = (By.ID, "message3")
        self.city_error = (By.ID, "message4")
        self.state_error = (By.ID, "message5")
        self.pinno_error = (By.ID, "message6")
        self.phoneno_error = (By.ID, "message7")
        self.mailid_error = (By.ID, "message9")
        self.password_error = (By.ID, "message18")
    
    def open_page(self, url):
        # Tìm phần tử có href chứa giá trị `url` và click để mở trang
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//a[contains(@href, '{url}')]"))
        )
        element.click()
        
    def enter_cusname(self, cusname):
        field = self.driver.find_element(*self.cusname_textbox)
        field.clear()
        field.send_keys(cusname)
    
    def enter_dob(self, dob):
        field = self.driver.find_element(*self.dob_textbox)
        field.clear()
        field.send_keys(dob)
    
    def enter_address(self, address):
        field = self.driver.find_element(*self.address_textbox)
        field.clear()
        field.send_keys(address)
    
    def enter_city(self, city):
        field = self.driver.find_element(*self.city_textbox)
        field.clear()
        field.send_keys(city)
    
    def enter_state(self, state):
        field = self.driver.find_element(*self.state_textbox)
        field.clear()
        field.send_keys(state)
    
    def enter_pinno(self, pinno):
        field = self.driver.find_element(*self.pinno_textbox)
        field.clear()
        field.send_keys(pinno)
    
    def enter_phoneno(self, phoneno):
        field = self.driver.find_element(*self.phoneno_textbox)
        field.clear()
        field.send_keys(phoneno)
    
    def enter_mailid(self, mailid):
        field = self.driver.find_element(*self.mailid_textbox)
        field.clear()    
        field.send_keys(mailid)    
    
    def enter_password(self, password):
        field = self.driver.find_element(*self.password_textbox)
        field.clear()
        field.send_keys(password)
    
    def click_submit(self):
        self.driver.find_element(*self.submit_button).click()
    
    def click_reset(self):
        self.driver.find_element(*self.reset_button).click()
    
    def find_element(self, *locator):
        return self.driver.find_element(*locator)
    
    def get_error_message(self, field_error_locator):
        return self.driver.find_element(*field_error_locator).text
    