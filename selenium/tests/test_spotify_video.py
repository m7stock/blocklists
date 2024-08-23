import configparser
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def test_play_youtube_video():
    config = configparser.ConfigParser()
    config.read('credentials.ini')

    chrome_options = Options()
    chrome_options.add_argument("--disable-search-engine-choice-screen")

    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 5)

    driver.get("https://open.spotify.com/show/7Co9FnIRkT2G9qD3ikH1nw")

    wait.until(
        EC.visibility_of_element_located((By.XPATH, "//button[@data-testid='login-button']"))
    ).click()
    wait.until(
        EC.visibility_of_element_located((By.XPATH, "//input[@id='login-username']"))
    ).send_keys(config['spotify']['username'])
    wait.until(
        EC.visibility_of_element_located((By.XPATH, "//input[@id='login-password']"))
    ).send_keys(config['spotify']['password'])
    wait.until(
        EC.visibility_of_element_located((By.XPATH, "//button[@id='login-button']"))
    ).click()
    wait.until(
        EC.visibility_of_element_located((By.XPATH, "//div[@data-testid='episode-0']//button[@data-testid='play-button']"))
    ).click()

    time.sleep(3)

    episode_title = wait.until(EC.visibility_of_element_located((By.XPATH, "//a[@data-encore-id='listRowTitle']"))).text
    video_title = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@data-testid='context-item-info-title']"))).text

    assert episode_title.strip(), "missing episode title"
    assert video_title != episode_title, "video is not blocked"
