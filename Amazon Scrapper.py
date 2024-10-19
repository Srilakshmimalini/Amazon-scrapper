from bs4 import BeautifulSoup
import requests
import csv
import time
import os

def get_title(soup):
    try:
        title = soup.find("span", attrs={"id": 'productTitle'})
        return title.string.strip() if title else ""
    except Exception:
        return ""

def get_price(soup):
    try:
        price = soup.find("span", attrs={'id': 'priceblock_ourprice'})
        return price.string.strip() if price else ""
    except Exception:
        return ""

def get_rating(soup):
    try:
        rating = soup.find("i", attrs={'class': 'a-icon a-icon-star a-star-4-5'})
        if rating:
            return rating.string.strip()
        rating_alt = soup.find("span", attrs={'class': 'a-icon-alt'})
        return rating_alt.string.strip() if rating_alt else ""
    except Exception:
        return ""

def get_review_count(soup):
    try:
        review_count = soup.find("span", attrs={'id': 'acrCustomerReviewText'})
        return review_count.string.strip() if review_count else ""
    except Exception:
        return ""

def get_availability(soup):
    try:
        available = soup.find("div", attrs={'id': 'availability'}).find("span")
        return available.string.strip() if available else ""
    except Exception:
        return ""

def scrape_product(URL):
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
        'Accept-Language': 'en-US, en;q=0.5'
    }

    try:
        webpage = requests.get(URL, headers=HEADERS)
        webpage.raise_for_status()
    except requests.RequestException as e:
        print(f"Request failed for {URL}: {e}")
        return ["", "", "", "", ""]

    soup = BeautifulSoup(webpage.content, "lxml")
    return [
        get_title(soup),
        get_price(soup),
        get_rating(soup),
        get_review_count(soup),
        get_availability(soup)
    ]

if _name_ == "_main_":  
    urls = [
        "https://www.amazon.com/Sony-PlayStation-Pro-1TB-Console-4/dp/B07K14XKZH/",
        "https://www.amazon.com/dp/B08FC5L3RG",
        "https://www.amazon.com/dp/B08FC6MR62",
        "https://www.amazon.com/Practical-Malware-Analysis-Hands-Dissecting/dp/1593272901/"
    ]

    filename = "amazon_products.xls"
   
    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Product Title", "Product Price", "Product Rating", "Number of Reviews", "Availability"])

            for url in urls:
                product_details = scrape_product(url)
                print(f"Scraping URL: {url}")
                print(product_details)
                writer.writerow(product_details)
                time.sleep(2)

        print(f"Data for all products has been written to {filename}")
    except PermissionError:
        print(f"Permission denied: Unable to write to file {filename}")
    except Exception as e:
        print(f"Failed to write to file: {e}")