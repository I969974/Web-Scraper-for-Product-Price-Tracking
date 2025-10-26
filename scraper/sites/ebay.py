import re
import requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"}


def parse_price_ebay(url: str) -> float:
    resp = requests.get(url, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "lxml")

    selectors = [
        '#prcIsum',
        '.notranslate',
        '.display-price',
        '.x-price-primary .x-price-int',
    ]
    text = None
    for sel in selectors:
        el = soup.select_one(sel)
        if el and el.get_text(strip=True):
            text = el.get_text(strip=True)
            break

    if not text:
        m = re.search(r"\$\s?[0-9,]+\.?[0-9]*|£\s?[0-9,]+\.?[0-9]*|€\s?[0-9,]+\.?[0-9]*", soup.get_text())
        if m:
            text = m.group(0)

    if not text:
        raise ValueError("Price not found on eBay page")

    price = re.sub(r"[^0-9.,]", "", text)
    price = price.replace(',', '')
    try:
        return float(price)
    except Exception as e:
        raise ValueError(f"Failed to parse price: {text}") from e
