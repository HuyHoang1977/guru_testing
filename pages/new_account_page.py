from selenium.webdriver.common.by import By

class NewAccountPage:

    def __init__(self, driver):
        self.driver = driver
        self.customer_id_textbox = (By.NAME, "cusid")
        self.account_type_combobox = (By.NAME, "selaccount")
        self.initial_deposit_textbox = (By.NAME, "inideposit")
        self.submit_button = (By.XPATH, "//input[@value='submit']")
        self.reset_button = (By.XPATH, "//input[@value='reset']")
    
    def open_page(self, url):
        self.driver.get(url)

    def enter_customer_id(self, customer_id):
        self.driver.find_element(*self.customer_id_textbox).send_keys(customer_id)

    def select_account_type(self, account_type):
        select_element = Select(self.driver.find_element(*self.account_type_combobox))
        select_element.select_by_visible_text(account_type)  # Select by visible text
    
    def enter_initial_deposit(self, initial_deposit):
        self.driver.find_element(*self.initial_deposit_textbox).send_keys(initial_deposit)

    def click_submit(self):
        self.driver.find_element(*self.submit_button).click()
        
    def click_reset(self):
        self.driver.find_element(*self.reset_button).click()