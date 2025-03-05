from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import requests
import os
import time
import random

# Set up Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--remote-debugging-port=9222")
chrome_options.add_argument("--disable-software-rasterizer")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-background-networking")
chrome_options.add_argument("--disable-sync")
chrome_options.add_argument("--disable-features=NetworkService,NetworkServiceInProcess")

# Use real Chrome profile
chrome_options.add_argument(r"--user-data-dir=C:\Users\felix\AppData\Local\Google\Chrome\User Data")
chrome_options.add_argument("--profile-directory=Default")  # Use actual profile from chrome://version/

# Kill any running Chrome instances before launching
os.system("taskkill /F /IM chrome.exe >nul 2>&1")

# Initialize WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Open the target page
driver.get("https://pte-core.com/podcast/read-aloud")

time.sleep(3)  # Wait for the page to load

# Retrieve cookies from the real Chrome session
cookies = driver.get_cookies()
cookie_header = "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])

# Directory to save files
save_dir = "音频资源/podcast/read-aloud"
os.makedirs(save_dir, exist_ok=True)


def download_audio(audio_url, file_name):
    """Download an audio file from the given URL."""
    headers = {
        "Referer": "https://pte-core.com/podcast/read-aloud",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
        "Accept": "*/*",
        "Range": "bytes=0-",
        "Cookie": cookie_header  # Inject real cookies
    }

    try:
        response = requests.get(audio_url, headers=headers, stream=True, timeout=10)
        if response.status_code == 200:
            with open(file_name, "wb") as audio_file:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        audio_file.write(chunk)
            print(f"Download complete: {file_name}")
        else:
            print(f"Failed to download {audio_url}. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Download error: {e}")


try:
    while True:
        # Find and intercept the audio file
        audio_elements = driver.find_elements(By.TAG_NAME, "audio")
        for audio in audio_elements:
            audio_url = audio.get_attribute("src")
            if audio_url and "mp3" in audio_url:
                file_name = os.path.join(save_dir, os.path.basename(audio_url))
                if not os.path.exists(file_name):  # Avoid duplicate downloads
                    print(f"Downloading: {audio_url}")
                    download_audio(audio_url, file_name)

        # Click the "Next" button to load a new question
        try:
            next_button = driver.find_element(By.XPATH,
                                              "/html/body/div[1]/div/main/div/div/div/div[2]/div/div/div/div[3]/button[3]")
            ActionChains(driver).move_to_element(next_button).click().perform()
            print("Navigating to the next question...")
        except Exception as e:
            print(f"Failed to find the 'Next' button: {e}")
            break

        # Randomized delay to avoid detection
        time.sleep(random.uniform(0.8, 1.2))

except KeyboardInterrupt:
    print("Download interrupted by user. Exiting.")
finally:
    driver.quit()