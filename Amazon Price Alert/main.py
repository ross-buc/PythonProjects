from bs4 import BeautifulSoup
import requests
from send_email import send_email


def main():
    # A dictionary with the product and price point to be searched

    product = {
        "Dell Laptop": {
            "Amazon_Url": "https://www.amazon.com.au/XPS7390-InfinityEdge-Touchscreen-i5-10210U-Windows/dp/B07ZSFXPZX",
            "Target_Price": 3000,
        }
    }

    # Using the request module to scrap the Amazon website

    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }

    response = requests.get(url=product["Dell Laptop"]["Amazon_Url"], headers=header)
    web_data = response.text

    # Using Beautiful Soup to create a searchable file

    soup = BeautifulSoup(web_data, "html.parser")

    # Searching the scrapped data for the current price

    amazon_current_price = soup.find("span", {"class": "a-price-whole"}).get_text()
    amazon_current_price_format = amazon_current_price.replace(",", "").replace(".", "")

    # For loop to see if the current price is lower than the target price

    if int(amazon_current_price_format) < int(product["Dell Laptop"]["Target_Price"]):
        print(
            f"The {list(product)[0]} is now ${amazon_current_price_format}. Sending email details..."
        )
        send_email(
            list(product)[0],
            amazon_current_price_format,
            product["Dell Laptop"]["Amazon_Url"],
        )


if __name__ == "__main__":
    main()
