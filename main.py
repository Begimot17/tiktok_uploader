import time
import os
import json
import pyautogui
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from seleniumwire import webdriver
from selenium_stealth import stealth

TIKTOK_UPLOAD_URL = "https://www.tiktok.com/tiktokstudio/upload"
ACCOUNTS_DIRECTORY = r"C:\Users\root\PycharmProjects\tiktok-loader\accounts"


def driver_init():
    options = webdriver.ChromeOptions()
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.199 Safari/537.36"
    )
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(options=options)

    stealth(
        driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )

    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {
            "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
        """
        },
    )
    return driver


def wait_and_click_button(driver, by, value, timeout=30):
    try:
        button = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((by, value))
        )
        button.click()
        print(f"Кнопка нажата: {value}")
    except Exception as e:
        print(f"Не удалось найти или нажать кнопку: {str(e)}")


def open_file(filepath):
    time.sleep(2)
    pyautogui.write(filepath)
    pyautogui.press("enter")


def update_json_status(file_path, file, status):
    json_file_path = os.path.join(os.path.dirname(file_path), "upload_status.json")
    if os.path.exists(json_file_path):
        with open(json_file_path, "r") as json_file:
            data = json.load(json_file)
    else:
        data = {}

    data[file] = status

    with open(json_file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)


def process_videos_in_directory(directory):
    for root, dirs, files in os.walk(directory):
        for account_dir in dirs:
            for account_root, account_dirs, account_files in os.walk(
                os.path.join(directory, str(account_dir))
            ):
                status_file_path = os.path.join(account_root, "upload_status.json")
                driver = driver_init()
                driver_start = False
                try:
                    for i, account_file in enumerate(account_files):
                        if account_file.lower().endswith((".mp4", ".mov", ".avi")):
                            file_path = os.path.join(account_root, account_file)

                            if os.path.exists(status_file_path):
                                with open(status_file_path, "r") as json_file:
                                    uploaded_files = json.load(json_file)
                            else:
                                uploaded_files = {}

                            if (
                                account_file in uploaded_files
                                and uploaded_files[account_file] == "uploaded"
                            ):
                                print(f"Файл уже загружен: {account_file}")
                                continue

                            print(f"Обработка файла: {account_file}")
                            if not driver_start:
                                driver_start = True
                                driver.get(TIKTOK_UPLOAD_URL)
                                driver.add_cookie({"name": "sessionid", "value": account_dir})
                                wait_and_click_button(
                                    driver,
                                    By.XPATH,
                                    "//div[contains(@class, 'TUXButton-label') and contains(text(), 'Select video')]",
                                )
                            open_file(file_path)

                            wait_and_click_button(
                                driver,
                                By.XPATH,
                                "//button[not(contains(@class, 'TUXButton--disabled'))]//div[contains(@class, 'TUXButton-label') and contains(text(), 'Post')]",
                            )
                            wait_and_click_button(
                                driver,
                                By.XPATH,
                                "//div[contains(@class, 'TUXButton-label') and contains(text(), 'Upload')]",
                            )
                            update_json_status(file_path, account_file, "uploaded")
                            if i != len(account_files) - 1:
                                wait_and_click_button(
                                    driver,
                                    By.CSS_SELECTOR,
                                    "div.upload-stage-container",
                                )

                finally:
                    driver.quit()


if __name__ == "__main__":
    process_videos_in_directory(ACCOUNTS_DIRECTORY)
