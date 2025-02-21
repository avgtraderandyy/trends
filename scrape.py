import time
import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# Set download directory
DOWNLOAD_DIR = "/app/downloads"

def get_google_trends():
    # Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-gpu")

    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": DOWNLOAD_DIR,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })

    # Manually specify the ChromeDriver path
    service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Define URLs and corresponding filenames
    time_ranges = {
        "4": "4htrends.csv",
        "24": "1dtrends.csv",
        "168": "7dtrends.csv"
    }

    for hours, filename in time_ranges.items():
        url = f"https://trends.google.com/trending?geo=US&hours={hours}"
        driver.get(url)
        time.sleep(5)  # Allow the page to load

        try:
            # Find the "Download CSV" button using the 'aria-label' attribute
            download_button = driver.find_element(By.XPATH, "//li[@aria-label='Download CSV']")
            driver.execute_script("arguments[0].click();", download_button)
            print(f"Download button clicked for {filename}!")

            # Wait for the file to download
            time.sleep(5)

            # Check if a CSV was downloaded
            files = os.listdir(DOWNLOAD_DIR)
            csv_files = [f for f in files if f.endswith(".csv")]
            
            if csv_files:
                downloaded_file = os.path.join(DOWNLOAD_DIR, csv_files[0])
                new_file = os.path.join(DOWNLOAD_DIR, filename)
                
                # Rename the downloaded file
                os.rename(downloaded_file, new_file)
                print(f"File renamed to {filename}")

            else:
                print("No CSV file found.")

        except Exception as e:
            print(f"Error: {e}")

    # Close the browser
    driver.quit()

def get_twitter_trends_data():
    try:
        print("Hello")
        # URL of the page to scrape
        url = "https://getdaytrends.com/united-states/"

        # Headers to mimic a browser visit
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }

        # Send the request
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        # Find both tables
        tables = soup.find_all("table", class_="table table-hover text-left clickable ranking trends wider mb-0")
        tables = tables + soup.find_all("table", class_="table table-hover text-left clickable ranking trends wider collapse")

        trends = []

        
        for table in tables:
            for row in table.find_all("tr"):
                rank_tag = row.find("th", class_="pos")  # Find rank in <th>
                main_tag = row.find("td", class_="main")  # Find trend name & tweets in <td>

                if rank_tag and main_tag:
                    rank = rank_tag.text.strip()  # Rank number
                    
                    # Extract trend name
                    trend_name_tag = main_tag.find("a")
                    trend_name = trend_name_tag.text.strip() if trend_name_tag else "Unknown"

                    # Extract tweet count safely
                    tweet_count_tag = main_tag.find("span", class_="small text-muted")
                    tweet_count = tweet_count_tag.text.strip() if tweet_count_tag else "N/A"

                    trends.append((rank, trend_name, tweet_count))

        # Print results
        for rank, trend, count in trends:
            print(f"{rank}. {trend} - {count} tweets")
    except Exception as e:
        print(e)

get_twitter_trends_data()
