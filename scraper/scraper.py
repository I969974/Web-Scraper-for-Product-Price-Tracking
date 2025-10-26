import importlib
import time
import os
from typing import Callable, Dict, Any

from .db import DB
from . import sites
from .alerts import send_email

SITE_FUNCS = {
    'amazon': sites.parse_price_amazon,
    'ebay': sites.parse_price_ebay,
}


def detect_site(url: str) -> str:
    url = url.lower()
    if 'amazon.' in url:
        return 'amazon'
    if 'ebay.' in url:
        return 'ebay'
    return 'generic'


def parse_generic(url: str) -> float:
    # Improved generic parser: try multiple patterns and selectors
    import re, requests
    from bs4 import BeautifulSoup
    HEADERS = {"User-Agent": os.getenv('USER_AGENT', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36')}
    resp = requests.get(url, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'lxml')
    
    # Try common price selectors first
    price_selectors = [
        '[data-price]', '.price', '.cost', '.amount', 
        '[class*="price"]', '[class*="cost"]', '[id*="price"]'
    ]
    
    for sel in price_selectors:
        els = soup.select(sel)
        for el in els:
            text = el.get_text(strip=True)
            # Look for currency patterns in this element
            m = re.search(r'[\$£€]\s?([0-9,]+\.?[0-9]*)', text)
            if m:
                price_str = m.group(1).replace(',', '')
                try:
                    return float(price_str)
                except ValueError:
                    continue
    
    # Fallback: search entire page text
    text = soup.get_text()
    matches = re.findall(r'[\$£€]\s?([0-9,]+\.?[0-9]*)', text)
    if matches:
        # Take the first reasonable price (between $1 and $10000)
        for match in matches:
            try:
                price = float(match.replace(',', ''))
                if 1.0 <= price <= 10000.0:
                    return price
            except ValueError:
                continue
    
    raise ValueError('Price not found (generic)')


class Scraper:
    def __init__(self, db_path: str = None):
        db_path = db_path or os.getenv('DATABASE_PATH', 'data.db')
        self.db = DB(db_path)

    def fetch_price(self, url: str) -> float:
        site = detect_site(url)
        func = SITE_FUNCS.get(site, parse_generic)
        return func(url)

    def check_all(self):
        targets = self.db.list_targets()
        alerts = []
        for tid, url, name, target_price in targets:
            try:
                price = self.fetch_price(url)
                prev = self.db.get_last_price(tid)
                self.db.record_price(tid, price)
                if (target_price is not None and price <= target_price) or (prev is not None and price < prev):
                    alerts.append((tid, url, name, price, prev))
            except Exception as e:
                print(f"Failed to fetch {url}: {e}")
        # send alerts
        for tid, url, name, price, prev in alerts:
            subj = f"Price alert: {name or url} now {price}"
            body = f"URL: {url}\nCurrent price: {price}\nPrevious price: {prev}\n"
            try:
                send_email(subj, body)
                print(f"Alert sent for {url}")
            except Exception as e:
                print(f"Failed to send alert for {url}: {e}")


if __name__ == '__main__':
    s = Scraper()
    s.check_all()
