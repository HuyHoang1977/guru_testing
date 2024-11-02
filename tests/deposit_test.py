from httpcore import TimeoutException
import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
sys.path.insert(1, 'D:\Code\Py\guru_testing\pages')
from deposit import DepositPage

@pytest.fixture()
def driver():
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.implicitly_wait(10)
    yield driver
    driver.close()
    driver.quit()
    
# TC1: Account No không để trống
def test_invalid_account_no(driver):
    deposit_page = DepositPage(driver)
    deposit_page.open_page("https://www.demo.guru99.com/V4/manager/DepositInput.php")
    accountno_input = driver.find_element(*deposit_page.accountno_textbox)
    accountno_input.click()

    accountno_input.send_keys(Keys.TAB)

    # Hiện thị lỗi
    error_message = driver.find_element(By.ID, "message2").text
    assert "Account Number must not be blank" in error_message
    
#  TC2: "Account No" không có kí tự chữ
def test_characters_in_account_no(driver):
    deposit_page = DepositPage(driver)
    deposit_page.open_page("https://www.demo.guru99.com/V4/manager/DepositInput.php")
    deposit_page.enter_accountno("abc")
    
    # Hiện thị lỗi
    error_message = driver.find_element(By.ID, "message2").text
    assert "Characters are not allowed" in error_message
    
# TC3: "Account No" không có kí tự đặc biệt
def test_special_characters_in_account_no(driver):
    deposit_page = DepositPage(driver)
    deposit_page.open_page("https://www.demo.guru99.com/V4/manager/DepositInput.php")
    deposit_page.enter_accountno("<")
    
    # Hiện thị lỗi
    error_message = driver.find_element(By.ID, "message2").text
    assert "Special characters are not allowed" in error_message
    
# TC4: "Account No" hợp lệ
def test_valid_account_no(driver):
    deposit_page = DepositPage(driver)
    deposit_page.open_page("https://www.demo.guru99.com/V4/manager/DepositInput.php")
    deposit_page.enter_accountno("139408")
    deposit_page.enter_amount(Keys.TAB)
    
    message = driver.find_element(By.ID, "message2").text
    assert "" in message

# TC5: Amount không để trống
def test_invalid_amount(driver):
    deposit_page = DepositPage(driver)
    deposit_page.open_page("https://www.demo.guru99.com/V4/manager/DepositInput.php")
    deposit_page.enter_amount(Keys.TAB)
    
    # Hiện thị lỗi
    error_message = driver.find_element(By.ID, "message1").text
    assert "Amount field must not be blank" in error_message

# TC 6: "Amount" không có kí tự chữ
def test_characters_in_amount(driver):
    deposit_page = DepositPage(driver)
    deposit_page.open_page("https://www.demo.guru99.com/V4/manager/DepositInput.php")
    deposit_page.enter_amount("abc")
    
    # Hiện thị lỗi
    error_message = driver.find_element(By.ID, "message1").text
    assert "Characters are not allowed" in error_message
    
# TC 7: "Amount" không có kí tự đặc biệt
def test_special_characters_in_amount(driver):
    deposit_page = DepositPage(driver)
    deposit_page.open_page("https://www.demo.guru99.com/V4/manager/DepositInput.php")
    deposit_page.enter_amount("<")
    
    # Hiện thị lỗi
    error_message = driver.find_element(By.ID, "message1").text
    assert "Special characters are not allowed" in error_message

# TC 8: "Amount" hợp lệ
def test_valid_amount(driver):
    deposit_page = DepositPage(driver)
    deposit_page.open_page("https://www.demo.guru99.com/V4/manager/DepositInput.php")
    deposit_page.enter_amount("10")
    deposit_page.enter_amount(Keys.TAB)
    
    message = driver.find_element(By.ID, "message1").text
    assert "" in message

# TC 9: Description không để trống
def test_invalid_description(driver):
    deposit_page = DepositPage(driver)
    deposit_page.open_page("https://www.demo.guru99.com/V4/manager/DepositInput.php")
    deposit_page.enter_description(Keys.TAB)
    
    # Hiện thị lỗi
    error_message = driver.find_element(By.ID, "message17").text
    assert "Description can not be blank" in error_message

# TC 10: Submit thành công
def test_submit_deposit(driver):
    deposit_page = DepositPage(driver)
    deposit_page.open_page("https://www.demo.guru99.com/V4/manager/DepositInput.php")
    deposit_page.enter_accountno("139408")
    deposit_page.enter_amount("10")
    deposit_page.enter_description("Test")
    deposit_page.click_submit()
    try:
        
        # Wait for the success message to appear
        success_message = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//p[contains(text(), 'Transaction details of Deposit')]"))
        )
        assert "Transaction details of Deposit" in success_message.text, "Deposit failed."
    except TimeoutException:
        pytest.fail("No success message displayed after submission.")

        
# TC 11: Người dùng có thể Reset
def test_reset(driver):
    deposit_page = DepositPage(driver)
    deposit_page.open_page("https://www.demo.guru99.com/V4/manager/DepositInput.php")
    deposit_page.enter_accountno("139408")
    deposit_page.enter_amount("10")
    deposit_page.enter_description("Test")
    deposit_page.click_reset()
    
    # Check fields are cleared
    accountno_input = driver.find_element(*deposit_page.accountno_textbox)
    amount_input = driver.find_element(*deposit_page.amount_textbox)
    description_input = driver.find_element(*deposit_page.description_textbox)
    
    assert accountno_input.get_attribute("value") == ""
    assert amount_input.get_attribute("value") == ""
    assert description_input.get_attribute("value") == ""