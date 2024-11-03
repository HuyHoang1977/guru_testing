from selenium.webdriver.common.by import By

class LoginPage:

    def __init__(self, driver):
        self.driver = driver
        self.username_textbox = (By.NAME, "uid")
        self.password_textbox = (By.NAME, "password")
        self.login_button = (By.XPATH, "//input[@value='LOGIN']")
        self.reset_button = (By.XPATH, "//input[@value='RESET']")
        
        # Locators for error messages (these IDs may vary depending on actual implementation)
        self.heading_successfully = (By.CLASS_NAME, "heading3")
        self.username_error = (By.ID, "message23")
        self.password_error = (By.ID, "message18")
    
    def open_page(self, url):
        self.driver.get(url)

    def enter_username(self, username):
        field = self.driver.find_element(*self.username_textbox)
        field.clear()
        field.send_keys(username)

    def enter_password(self, password):
        field = self.driver.find_element(*self.password_textbox)
        field.clear()
        field.send_keys(password)

    def click_login(self):
        self.driver.find_element(*self.login_button).click()
        
    def click_reset(self):
        self.driver.find_element(*self.reset_button).click()
    
    def get_error_message(self, field_error_locator):
        return self.driver.find_element(*field_error_locator).text
    
    def get_success_message(self, field_success_locator):
        return self.driver.find_element(*field_success_locator).text
    
    def find_element(self, *locator):
        return self.driver.find_element(*locator)