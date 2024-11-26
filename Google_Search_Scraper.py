
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import pandas as pd

# Step 1: Set up Selenium WebDriver
def setup_driver():
    # Update the path to where you downloaded ChromeDriver
    driver_path = "path_to_chromedriver"
    driver = webdriver.Chrome(driver_path)
    return driver

# Step 2: Perform Google Search
def google_search(driver, query):
    driver.get("https://www.google.com")
    time.sleep(2)

    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
    time.sleep(3)  # Wait for results to load

    return driver.page_source

# Step 3: Extract Data with BeautifulSoup
def parse_results(html):
    soup = BeautifulSoup(html, "html.parser")
    results = []

    for result in soup.find_all("div", class_="tF2Cxc"):
        title = result.find("h3").text if result.find("h3") else "No title"
        link = result.find("a")["href"] if result.find("a") else "No link"
        snippet = result.find("span", class_="aCOpRe").text if result.find("span", class_="aCOpRe") else "No snippet"
        results.append({"Title": title, "Link": link, "Description": snippet})

    return results

# Step 4: Save Results to CSV
def save_to_csv(data, filename="google_results.csv"):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Results saved to {filename}")

# Main Program
if __name__ == "__main__":
    query = input("Enter your search query: ")
    driver = setup_driver()

    try:
        html = google_search(driver, query)
        results = parse_results(html)
        save_to_csv(results)
        driver.quit()
    except Exception as e:
        print(f"An error occurred: {e}")
        driver.quit()
