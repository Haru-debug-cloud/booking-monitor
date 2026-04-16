from pathlib import Path
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

TARGETS_FILE = "targets.csv"

def main():
    targets = pd.read_csv(TARGETS_FILE)

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    try:
        for _, row in targets.iterrows():
            space_name = row["space_name"]
            url = row["url"]

            driver.get(url)
            driver.implicitly_wait(10)

            html = driver.page_source
            file_name = f"page_source_{space_name}.html"
            Path(file_name).write_text(html, encoding="utf-8")

            print(f"saved: {file_name}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
