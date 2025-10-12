# test_sprint3.py
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://travner.vercel.app"

# -------------------
# HELPER FUNCTION
# -------------------
def wait_for_element(driver, by, locator, timeout=10):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, locator))
    )

# -------------------
# SPRINT 3 TESTS
# -------------------

def test_status_post_with_tag(driver):
    """TST-013: Post a status with tagged friend"""
    driver.get(BASE_URL + "/social")
    status_box = wait_for_element(driver, By.ID, "status-box")
    status_box.send_keys("Having fun with @friend123")
    driver.find_element(By.ID, "post-btn").click()

    feed = wait_for_element(driver, By.ID, "feed")
    assert "@friend123" in feed.text, "Friend tag not visible in post"


def test_status_post_with_emoji(driver):
    """TST-014: Post a status with emoji"""
    driver.get(BASE_URL + "/social")
    status_box = wait_for_element(driver, By.ID, "status-box")
    status_box.send_keys("Good Morning ☀️")
    driver.find_element(By.ID, "post-btn").click()

    feed = wait_for_element(driver, By.ID, "feed")
    assert "☀️" in feed.text, "Emoji not rendered in post"


def test_scheduled_post(driver):
    """TST-015: Schedule a post"""
    driver.get(BASE_URL + "/social")
    status_box = wait_for_element(driver, By.ID, "status-box")
    status_box.send_keys("This is a scheduled post")

    driver.find_element(By.ID, "schedule-btn").click()
    time_picker = wait_for_element(driver, By.ID, "schedule-time")
    time_picker.send_keys("2025-09-25 10:00")

    driver.find_element(By.ID, "save-schedule-btn").click()

    msg = wait_for_element(driver, By.ID, "schedule-success")
    assert msg.is_displayed(), "Schedule success message not shown"


def test_single_photo_upload(driver):
    """TST-016: Upload a single photo"""
    driver.get(BASE_URL + "/social")
    upload_input = wait_for_element(driver, By.ID, "photo-upload")
    upload_input.send_keys(r"C:\Users\Abdullah Ayman Azaan\Documents\sample.jpg")

    driver.find_element(By.ID, "post-btn").click()
    feed_img = wait_for_element(driver, By.TAG_NAME, "img")

    assert feed_img.is_displayed(), "Uploaded photo not visible"


def test_multi_photo_upload(driver):
    """TST-017: Upload multiple photos"""
    driver.get(BASE_URL + "/social")
    upload_input = wait_for_element(driver, By.ID, "photo-upload")
    upload_input.send_keys(
        r"C:\Users\Abdullah Ayman Azaan\Documents\sample1.jpg\n"
        r"C:\Users\Abdullah Ayman Azaan\Documents\sample2.jpg"
    )

    driver.find_element(By.ID, "post-btn").click()
    photos = driver.find_elements(By.TAG_NAME, "img")

    assert len(photos) >= 2, "Multiple photos not uploaded"


def test_short_video_with_filter(driver):
    """TST-018: Upload short video with filter"""
    driver.get(BASE_URL + "/social")
    video_input = wait_for_element(driver, By.ID, "video-upload")
    video_input.send_keys(r"C:\Users\Abdullah Ayman Azaan\Documents\sample.mp4")

    driver.find_element(By.ID, "filter-btn").click()
    driver.find_element(By.ID, "post-btn").click()

    video = wait_for_element(driver, By.TAG_NAME, "video")
    assert video.is_displayed(), "Video not visible after posting"


def test_video_with_captions(driver):
    """TST-019: Upload video with captions"""
    driver.get(BASE_URL + "/social")
    video_input = wait_for_element(driver, By.ID, "video-upload")
    video_input.send_keys(r"C:\Users\Abdullah Ayman Azaan\Documents\sample.mp4")

    caption_input = wait_for_element(driver, By.ID, "video-caption")
    caption_input.send_keys("This is my caption")

    driver.find_element(By.ID, "post-btn").click()
    feed = wait_for_element(driver, By.ID, "feed")

    assert "This is my caption" in feed.text, "Caption not visible in video post"
