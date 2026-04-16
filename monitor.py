from datetime import datetime
from pathlib import Path
import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

TARGET_URL = "https://www.instabase.jp/space/5750329482"
OUTPUT_FILE = "monitor_log.csv"


def get_page_text(url: str) -> str:
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    try:
        driver.get(url)
        driver.implicitly_wait(10)
        body = driver.find_element(By.TAG_NAME, "body").text
        return body
    finally:
        driver.quit()


def judge_status(page_text: str) -> str:
    if "予約不可" in page_text or "満室" in page_text:
        return "full"
    if "予約可能" in page_text or "空室" in page_text:
        return "available"
    return "unknown"


def main():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    page_text = get_page_text(TARGET_URL)
    status = judge_status(page_text)

    row = pd.DataFrame([{
        "timestamp": now,
        "space_name": "instabase_test",
        "url": TARGET_URL,
        "status": status
    }])

    output_path = Path(OUTPUT_FILE)
    if output_path.exists():
        old_df = pd.read_csv(output_path)
        row = pd.concat([old_df, row], ignore_index=True)

    row.to_csv(output_path, index=False, encoding="utf-8-sig")
    print("saved")


if __name__ == "__main__":
    main()
