import time
import undetected_chromedriver as uc

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common import WebDriverException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from env_stash import DRIVER_PATH, CHROME_PATH, PROFILE_DIR, USER_DATA_DIR, PARSING_PATH


def setUp() -> WebDriver | None:
    """Setting up driver with headers"""
    try:
        options = set_options(browser="Chrome")
        driver = uc.Chrome(options=options, driver_executable_path=DRIVER_PATH, browser_executable_path=CHROME_PATH)
        driver.maximize_window()

        return driver
    except WebDriverException as e:
        print("Произошла ошибка при инициализации драйвера:", e)
        return None
    except Exception as e:
        print("Произошла неожиданная ошибка:", e)
        return None


def set_options(browser: str = 'Chrome') -> (
        webdriver.ChromeOptions | webdriver.SafariOptions | webdriver.FirefoxOptions):
    """Sets options for your driver"""
    try:
        match browser:
            case "Chrome":
                options = webdriver.ChromeOptions()
            case "Safari":
                options = webdriver.SafariOptions()
            case "Firefox":
                options = webdriver.FirefoxOptions()
            case _:
                raise Exception("Wrong browser specified. Can't create options")

        options.add_argument(f"--user-data-dir={USER_DATA_DIR}")
        options.add_argument(f"--profile-directory={PROFILE_DIR}")

        return options

    except Exception as e:
        print(e)


def establish_connection(driver: WebDriver) -> WebDriverWait:
    """Waiting to load full page"""
    wait = WebDriverWait(driver, 10)
    wait.until(EC.number_of_windows_to_be(1))

    driver.get(PARSING_PATH)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.XPATH, '//*[@id="a11y-main-content"]/div[2]/div/div/div/h2/span/a')))

    return wait


def scroll_page(driver) -> True:
    """Script for loading all hh scripts, as by def they give 20 posts. After this there'll be 30 more."""
    height = driver.execute_script("return document.body.scrollHeight")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    time.sleep(3)
    driver.execute_script("window.scrollTo(0, 0);")

    return True
