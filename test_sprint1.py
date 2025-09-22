# test_sprint1_stable_full.py
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

BASE_URL = "https://travner.vercel.app"

# -------------------
# TEST DATA (edit here only)
# -------------------
TEST_DATA = {
    "email": "joy@gmail.com",
    "password": "joy2001",
    "new_password": "joy123456",
    "wrong_password": "joy234",
    "otp": "123456",
    "dummy_file": r"file:///D:/Travner%20Automation/Test/Automation_Test_Report_Sprint1.pdf"
}

# -------------------
# HELPER FUNCTIONS
# -------------------

def wait_for_element(driver, by, locator, timeout=15):
    """Wait for element to be visible and return it."""
    try:
        return WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((by, locator))
        )
    except TimeoutException:
        print(f"Timeout: Element {locator} not found")
        return None

def click_element(driver, by, locator, timeout=15):
    """Wait for element to be clickable and click."""
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((by, locator))
        )
        element.click()
        return True
    except TimeoutException:
        print(f"Timeout: Clickable element {locator} not found")
        return False

def login_user(driver, email, password):
    """Perform email/password login."""
    driver.get(BASE_URL + "/login")
    email_input = wait_for_element(driver, By.ID, "email")
    password_input = wait_for_element(driver, By.ID, "current-password")
    login_btn = wait_for_element(driver, By.ID, "login-btn")

    if email_input and password_input and login_btn:
        email_input.clear()
        email_input.send_keys(email)
        password_input.clear()
        password_input.send_keys(password)
        login_btn.click()
    else:
        print("Login failed: missing elements")

# -------------------
# TEST CASES
# -------------------

def test_social_signup_google(driver):
    driver.get(BASE_URL + "/signup")
    if click_element(driver, By.ID, "google-signup-btn"):
        print("Google signup test - manual verification required")
        time.sleep(2)

def test_guide_signup_facebook(driver):
    driver.get(BASE_URL + "/guide-signup")
    if click_element(driver, By.ID, "facebook-signup-btn"):
        print("Facebook signup test - manual verification required")
        time.sleep(2)

def test_guide_signup_document(driver):
    """Guide signup document upload test."""
    driver.get(BASE_URL + "/guide-signup")
    upload_input = wait_for_element(driver, By.ID, "document-upload")
    submit_btn = wait_for_element(driver, By.ID, "submit-guide-signup")
    
    if not upload_input or not submit_btn:
        print("Document upload elements not found!")
        assert False, "Missing document upload elements"

    upload_input.send_keys(TEST_DATA["dummy_file"])
    submit_btn.click()
    
    success_msg = wait_for_element(driver, By.ID, "signup-success")
    assert success_msg is not None, "Signup success message not found"
    assert success_msg.is_displayed(), "Signup success message not visible"

def test_password_strength(driver):
    """Signup weak password validation."""
    driver.get(BASE_URL + "/signup")
    password_input = wait_for_element(driver, By.ID, "password")
    submit_btn = wait_for_element(driver, By.ID, "signup-btn")
    
    if not password_input or not submit_btn:
        print("Password input or signup button not found!")
        assert False, "Missing elements for password test"
    
    password_input.send_keys("weak")
    submit_btn.click()
    
    error_msg = wait_for_element(driver, By.ID, "password-error")
    assert error_msg is not None, "Password error message not found"
    assert error_msg.is_displayed(), "Password error message not visible"

def test_account_lockout(driver):
    """Test account lockout after multiple failed login attempts."""
    driver.get(BASE_URL + "/login")
    for _ in range(5):
        email_input = wait_for_element(driver, By.ID, "email")
        password_input = wait_for_element(driver, By.ID, "current-password")
        login_btn = wait_for_element(driver, By.ID, "login-btn")
        
        if not email_input or not password_input or not login_btn:
            print("Login elements not found!")
            assert False, "Missing elements for account lockout test"
        
        email_input.clear()
        password_input.clear()
        email_input.send_keys(TEST_DATA["email"])
        password_input.send_keys(TEST_DATA["wrong_password"])
        login_btn.click()
        time.sleep(1)
    
    lock_msg = wait_for_element(driver, By.ID, "lockout-msg")
    assert lock_msg is not None, "Lockout message not found"
    assert lock_msg.is_displayed(), "Lockout message not visible"

def test_traveller_login_email(driver):
    """Traveller email/password login test."""
    login_user(driver, TEST_DATA["email"], TEST_DATA["password"])
    dashboard = wait_for_element(driver, By.ID, "dashboard")
    assert dashboard is not None, "Dashboard not found after login"
    assert dashboard.is_displayed(), "Dashboard not visible after login"

def test_traveller_login_otp(driver):
    """Traveller OTP login test."""
    driver.get(BASE_URL + "/login")
    click_element(driver, By.ID, "otp-login-btn")
    otp_input = wait_for_element(driver, By.ID, "otp-input")
    submit_btn = wait_for_element(driver, By.ID, "submit-otp-btn")
    
    if not otp_input or not submit_btn:
        print("OTP input or submit button not found!")
        assert False, "Missing elements for OTP login test"
    
    otp_input.send_keys(TEST_DATA["otp"])
    submit_btn.click()
    
    dashboard = wait_for_element(driver, By.ID, "dashboard")
    assert dashboard is not None, "Dashboard not found after OTP login"
    assert dashboard.is_displayed(), "Dashboard not visible after OTP login"

def test_forgot_password(driver):
    """Forgot password flow."""
    driver.get(BASE_URL + "/login")
    click_element(driver, By.LINK_TEXT, "Forgot Password?")
    
    reset_form = wait_for_element(driver, By.ID, "reset-password-form")
    assert reset_form is not None, "Reset password form not found"
    assert reset_form.is_displayed(), "Reset password form not visible"

    # Enter email for reset
    email_input = wait_for_element(driver, By.ID, "reset-email")
    submit_btn = wait_for_element(driver, By.ID, "reset-submit-btn")
    
    if email_input and submit_btn:
        email_input.send_keys(TEST_DATA["email"])
        submit_btn.click()
        print("Password reset request submitted for:", TEST_DATA["email"])
    else:
        assert False, "Forgot password email input or submit button missing"

def test_change_password(driver):
    """Change password flow."""
    login_user(driver, TEST_DATA["email"], TEST_DATA["password"])
    click_element(driver, By.ID, "profile-menu")
    click_element(driver, By.ID, "change-password-btn")
    
    old_pass = wait_for_element(driver, By.ID, "old-password")
    new_pass = wait_for_element(driver, By.ID, "new-password")
    confirm_pass = wait_for_element(driver, By.ID, "confirm-password")
    submit_btn = wait_for_element(driver, By.ID, "submit-change-password")
    
    if not old_pass or not new_pass or not confirm_pass or not submit_btn:
        print("Change password elements not found!")
        assert False, "Missing elements for change password test"
    
    old_pass.send_keys(TEST_DATA["password"])
    new_pass.send_keys(TEST_DATA["new_password"])
    confirm_pass.send_keys(TEST_DATA["new_password"])
    submit_btn.click()
    
    success_msg = wait_for_element(driver, By.ID, "success-msg")
    assert success_msg is not None, "Change password success message not found"
    assert success_msg.is_displayed(), "Change password success message not visible"
