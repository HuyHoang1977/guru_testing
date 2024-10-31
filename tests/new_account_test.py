import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import sys
sys.path.insert(1, 'D://Subject//Testing//testing_assignment//pages')
from new_account_page import NewAccountPage


@pytest.fixture()
def driver():
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.implicitly_wait(10)
    yield driver
    driver.close()
    driver.quit()
    
# TC1: Customer ID không để trống
def test_invalid_customer_id(driver):
    new_account = NewAccountPage(driver)
    new_account.open_page("https://www.demo.guru99.com/V4/manager/addAccount.php")
    cusid_input = driver.find_element(*new_account.customer_id_textbox)
    cusid_input.click()
    
    cusid_input.send_keys(Keys.TAB)
    
    # Hiển thị lỗi
    error_message = driver.find_element(By.ID, "message14").text
    assert "Customer ID is required" in error_message

# TC2: "Customer ID" không có kí tự chữ
def test_characters_in_cusid(driver):
    new_account = NewAccountPage(driver)
    new_account.open_page("https://www.demo.guru99.com/V4/manager/addAccount.php")
    new_account.enter_customer_id("abc")
    
    # Hiển thị lỗi
    error_message = driver.find_element(By.ID, "message14").text
    assert "Characters are not allowed" in error_message

# TC3: "Customer ID" có kí tự đặc biệt
def test_special_characters_in_cusid(driver):
    new_account = NewAccountPage(driver)
    new_account.open_page("https://www.demo.guru99.com/V4/manager/addAccount.php")
    cusid_input = driver.find_element(*new_account.customer_id_textbox)
    new_account.enter_customer_id("<")
    
    # Hiển thị lỗi
    error_message = driver.find_element(By.ID, "message14").text
    assert "Special characters are not allowed" in error_message

# TC4: "Customer ID" kí tự đầu không được là khoảng trắng
def test_space_in_cusid(driver):
    new_account = NewAccountPage(driver)
    new_account.open_page("https://www.demo.guru99.com/V4/manager/addAccount.php")
    cusid_input = driver.find_element(*new_account.customer_id_textbox)
    new_account.enter_customer_id(" ")
    
    # Hiển thị lỗi
    error_message = driver.find_element(By.ID, "message14").text
    assert "First character can not have space" in error_message

# TC5: "Customer ID" hợp lệ
def test_valid_cusid(driver):
    new_account = NewAccountPage(driver)
    new_account.open_page("https://www.demo.guru99.com/V4/manager/addAccount.php")
    cusid_input = driver.find_element(*new_account.customer_id_textbox)
    new_account.enter_customer_id("57747")
    
    new_account.enter_customer_id(Keys.TAB)
    
    # Hiển thị lỗi
    error_message = driver.find_element(By.ID, "message14").text
    assert "" in error_message
    
# TC6: Submit thành công   
def test_submit(driver):
    new_account = NewAccountPage(driver)
    new_account.open_page("https://www.demo.guru99.com/V4/manager/addAccount.php")
    new_account.enter_customer_id("57747")
    new_account.enter_initial_deposit("1234567")
    new_account.click_submit()
    
# TC7: Người dùng có thể Reset
def test_reset(driver):
    new_account = NewAccountPage(driver)
    new_account.open_page("https://www.demo.guru99.com/V4/manager/addAccount.php")
    new_account.enter_customer_id("57747")
    new_account.enter_initial_deposit("1234567")
    new_account.click_reset()
    
    # Check fields are cleared
    cusid_input = driver.find_element(*new_account.customer_id_textbox)
    deposit_input = driver.find_element(*new_account.initial_deposit_textbox)
    account_type_input = driver.find_element(*new_account.account_type_combobox)
    
    assert cusid_input.get_attribute("value") == ""
    assert deposit_input.get_attribute("value") == ""
    assert account_type_input.get_attribute("value") == "Savings"
    