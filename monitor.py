from pathlib import Path
from datetime import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

TARGETS_FILE = "targets.csv"
OUTPUT_FILE = "iframes.csv"

def main():
    targets = pd.read_csv(TARGETS_FILE)

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    rows = []

    try:
        for _, row in targets.iterrows():
            space_name = row["space_name"]
            url = row["url"]

            driver.get(url)
            driver.implicitly_wait(10)
            
# カレンダーボタン押す
try:
    button = driver.find_element(By.XPATH, "//button[contains(., '空室カレンダー')]")
    button.click()
    driver.implicitly_wait(5)
except:
    pass
            iframes = driver.find_elements(By.TAG_NAME, "iframe")

            if not iframes:
                rows.append({
                    "checked_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "space_name": space_name,
                    "page_url": url,
                    "iframe_index": "",
                    "iframe_src": "NO_IFRAME"
                })
            else:
                for i, iframe in enumerate(iframes):
                    rows.append({
                        "checked_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "space_name": space_name,
                        "page_url": url,
                        "iframe_index": i,
                        "iframe_src": iframe.get_attribute("src")
                    })

        pd.DataFrame(rows).to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")
        print(f"saved: {OUTPUT_FILE}")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
