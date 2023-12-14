import requests
from bs4 import BeautifulSoup
import lxml
import smtplib
from dotenv import load_dotenv
import os

load_dotenv()

headers = {
    "User-Agent": "Defined",
    "Accept-Language": "en-US",
}

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
TARGET_EMAIL = os.getenv("TARGET_EMAIL")

URL = "https://www.amazon.com/Gundam-Epyon-Bandai-Spirits-Model/dp/B0BYYJHHWN/ref=sr_1_5?crid=1A4NZ3990YL1N&keywords=gundam&qid=1702558935&sprefix=gundam+%2Caps%2C339&sr=8-5"

response = requests.get(url=URL, headers=headers)
amazon_page = response.text

soup = BeautifulSoup(amazon_page, "lxml")
price = soup.select_one(".a-offscreen").get_text()
just_price = float(price.split("$")[1])
product_name = soup.find(name="span", id="productTitle").get_text().strip()

if just_price <= 54:
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=EMAIL, password=PASSWORD)
        connection.sendmail(
            from_addr=EMAIL,
            to_addrs=TARGET_EMAIL,
            msg=f"Subject:Amazon Lower Price Alert!\n\n{product_name} is ${just_price}\n{URL}".encode('utf-8')
        )