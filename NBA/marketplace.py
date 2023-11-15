import os
import time
import csv
from datetime import datetime
from bs4 import BeautifulSoup
import questionary
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def auto_click_more(driver, click_count):
    scroll_pause_time = 2
    total_height = driver.execute_script("return document.body.scrollHeight")
    button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[text()='Load more']"))
    )

    for _ in range(click_count):
        # Scroll down to the bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait for the page to load
        time.sleep(scroll_pause_time)

        # Check if the button is visible
        if button.is_displayed():
            button.click()

        # Calculate the new scroll height and check if we have reached the bottom
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == total_height:
            break
        total_height = new_height


def scrape_data():
    options = {
        "5": 5,
        "10": 10,
        "20": 20,
        "50": 50,
    }
    selected = questionary.select(
        "Please select the number of data pages you want to obtain:", options
    ).ask()

    print("Please wait ...")

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("blink-settings=imagesEnabled=false")  # dont show image
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    chrome_options.add_argument("--ignore-certificate-errors")
    driver = webdriver.Chrome(options=chrome_options)

    driver.get("https://www.nbatopshot.com/search?")

    try:
        # Wait for the elements to load
        time.sleep(12)  # You can adjust the waiting time here if needed

        auto_click_more(driver, int(selected))

        # Get the page source after scrolling
        page_source = driver.page_source

        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(page_source, "html.parser")

        current_date = datetime.now()

        formatted_date = current_date.strftime("%m%d%Y")
        
        WORKPATH = os.getcwd()
        CSVPATH = f"{WORKPATH}/topshot_data_{formatted_date}.csv"
        if not os.path.exists(CSVPATH):
            with open(CSVPATH, "w", newline="", encoding="utf-8") as w:
                writer = csv.DictWriter(
                    w,
                    fieldnames=[
                        "link",
                        "common",
                        "name",
                        "lowest_ask",
                        "avg_sale",
                        "hook_shot",
                    ],
                )
                writer.writeheader()

        data = []
        data_counter = 0

        for block in soup.select(".css-1850lbl > div"):
            link = block.select_one(".chakra-linkbox__overlay")
            if link:
                link = block.select_one(".chakra-linkbox__overlay").get("href")
            else:
                continue

            common = block.select_one(".css-1kgpxnt")
            if common:
                common = block.select_one(".css-1kgpxnt").get_text()
            else:
                continue

            name = block.select_one(".chakra-heading")
            if name:
                name = block.select_one(".chakra-heading").get_text()
            else:
                continue

            lowest_ask = block.select_one(".css-1hwxzsy")
            if lowest_ask:
                lowest_ask = block.select_one(".css-1hwxzsy").get_text()
            else:
                continue

            avg_sale = block.select_one(".css-zv2k34")
            if avg_sale:
                avg_sale = block.select_one(".css-zv2k34").get_text()
            else:
                continue

            hook_shot = block.select_one(".css-1kywzd4")
            if hook_shot:
                hook_shot = block.select_one(".css-1kywzd4").get_text()
            else:
                continue

            data.append(
                {
                    "link": f"https://www.nbatopshot.com{link}",
                    "common": common,
                    "name": name,
                    "name": name,
                    "lowest_ask": lowest_ask,
                    "avg_sale": avg_sale,
                    "hook_shot": hook_shot,
                }
            )
            data_counter += 1

        with open(CSVPATH, "+a", newline="", encoding="utf-8") as w:
            writer = csv.DictWriter(
                w,
                fieldnames=[
                    "link",
                    "common",
                    "name",
                    "lowest_ask",
                    "avg_sale",
                    "hook_shot",
                ],
            )
            writer.writerows(data)
            print(
                f"\033[31m{data_counter}\033[0m items of data have been saved, and the file path is:[\033[32m{CSVPATH}\033[0m]"
            )

    except Exception as e:
        print(e)
    finally:
        driver.quit()


scrape_data()
