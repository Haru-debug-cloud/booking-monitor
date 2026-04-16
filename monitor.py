from pathlib import Path
from datetime import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

TARGETS_FILE = "targets.csv"
OUTPUT_FILE = "page_texts.csv"

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

            body_text = driver.find_element(By.TAG_NAME, "body").text

            rows.append({
                "checked_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "space_name": space_name,
                "url": url,
                "page_text": body_text
            })

        out_df = pd.DataFrame(rows)
        out_df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")
        print(f"saved: {OUTPUT_FILE}")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
