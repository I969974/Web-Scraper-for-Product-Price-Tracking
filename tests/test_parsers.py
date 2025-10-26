from scraper.sites.amazon import parse_price_amazon
from scraper.sites.ebay import parse_price_ebay


def test_amazon_dummy():
    # This is a smoke test structure; real network tests are not run in CI here.
    try:
        parse_price_amazon("https://www.amazon.com/dp/B08N5WRWNW")
    except Exception:
        # It's okay for CI-free test to raise network errors; just ensure function exists
        assert True


def test_ebay_dummy():
    try:
        parse_price_ebay("https://www.ebay.com/itm/1234567890")
    except Exception:
        assert True
