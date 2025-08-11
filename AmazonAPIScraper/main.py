from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def scrape_amazon_product_selenium(product_url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run headless, remove if you want to see browser
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(product_url)

    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.ID, "productTitle")))

    title_elem = driver.find_element(By.ID, "productTitle")
    title = title_elem.text.strip()

    # Price extraction
    price_whole = ""
    price_fraction = ""
    try:
        price_whole_elem = driver.find_element(By.CSS_SELECTOR, "span.a-price-whole")
        price_whole = price_whole_elem.text.replace(",", "").strip()
    except:
        pass

    try:
        price_fraction_elem = driver.find_element(By.CSS_SELECTOR, "span.a-price-fraction")
        price_fraction = price_fraction_elem.text.strip()
    except:
        pass

    price = "N/A"
    if price_whole:
        price = f"£{price_whole}"
        if price_fraction:
            price += f".{price_fraction}"

    # Rating extraction
    rating = "N/A"
    try:
        rating_elem = driver.find_element(By.CSS_SELECTOR, "span[data-hook='rating-out-of-text']")
        rating = rating_elem.text.strip()
    except:
        try:
            rating_elem = driver.find_element(By.ID, "acrPopover")
            rating = rating_elem.get_attribute("title").strip()  # e.g. "4.5 out of 5 stars"
        except:
            pass

    print(f"Title: {title}")
    print(f"Price: {price}")
    print(f"Rating: {rating}")

    driver.quit()

if __name__ == "__main__":
    url = input("Enter Amazon product URL: ")
    scrape_amazon_product_selenium(url)






