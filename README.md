# Web Scraper - Price Alerts

This project scrapes product pages (Amazon, eBay, etc.) and stores price history. It can send email alerts when prices drop and includes a Streamlit dashboard to view price history.

## Features

- ✅ Scrapes prices from Amazon, eBay, and generic sites
- ✅ SQLite database for price history storage
- ✅ Email alerts when prices drop or hit target thresholds
- ✅ Streamlit dashboard for price visualization
- ✅ CLI for managing targets
- ✅ Configurable check intervals
- ✅ Environment-based configuration

## Quick Start

### 1. Install Dependencies

```bash
# Option A: Using virtualenv (recommended)
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Option B: System/user install
pip3 install --user -r requirements.txt
```

### 2. Configuration

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
# Edit .env with your SMTP settings
```

Required SMTP settings in `.env`:
```
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASS=your_app_password
FROM_EMAIL=your_email@gmail.com
TO_EMAIL=alerts@yourdomain.com
```

### 3. Add Products to Track

```bash
# Add a product with target price
python3 manage_targets.py add "https://www.amazon.com/dp/PRODUCTID" --name "Product Name" --target 29.99

# List all targets
python3 manage_targets.py list

# Remove a target by ID
python3 manage_targets.py remove 1
```

### 4. Run Price Checks

```bash
# Single check (good for testing)
python3 run_scraper.py --once

# Continuous monitoring (default: every 60 minutes)
python3 run_scraper.py

# Custom interval (every 30 minutes)
python3 run_scraper.py --interval 30
```

### 5. View Dashboard

```bash
# Start Streamlit dashboard
python3 -m streamlit run streamlit_app.py

# Access at http://localhost:8501
```

## Testing

Run the included tests:

```bash
pytest -v
```

## Important Limitations & Legal Notes

⚠️ **Legal Compliance**: Web scraping may violate Terms of Service of target websites. Always:
- Check robots.txt and ToS before scraping
- Use official APIs when available (Amazon Product Advertising API, eBay API)
- Respect rate limits and implement delays
- Consider the website's business impact

⚠️ **Technical Limitations**:
- **Anti-bot measures**: Many sites use Captchas, IP blocking, and dynamic content
- **HTML changes**: Site structure changes frequently, breaking parsers
- **Rate limiting**: Aggressive scraping can trigger IP bans

## Production Recommendations

For robust production use, consider:

### 1. Use Official APIs
- Amazon Product Advertising API
- eBay Developer APIs
- Other official product APIs

### 2. Advanced Scraping (if APIs unavailable)
```bash
# Install additional packages for robust scraping
pip install selenium playwright requests-html

# Use rotating proxies and user agents
pip install requests[socks] fake-useragent
```

### 3. Infrastructure Improvements
- **Proxy rotation**: Use services like ProxyMesh, Bright Data
- **Headless browsers**: Selenium/Playwright for dynamic content
- **Request delays**: Add random delays between requests
- **Error handling**: Implement exponential backoff
- **Monitoring**: Add logging and health checks

### 4. Deployment Options
```bash
# Docker deployment
docker build -t price-scraper .
docker run -d --env-file .env price-scraper

# Cron job for periodic checks
0 */6 * * * cd /path/to/scraper && python3 run_scraper.py --once

# Systemd service for continuous monitoring
sudo cp price-scraper.service /etc/systemd/system/
sudo systemctl enable price-scraper
```

## Architecture

```
scraper/
├── __init__.py          # Package initialization  
├── db.py               # SQLite database wrapper
├── scraper.py          # Main orchestration logic
├── alerts.py           # Email notification sender
└── sites/              # Site-specific parsers
    ├── __init__.py
    ├── amazon.py       # Amazon price parser
    └── ebay.py         # eBay price parser

manage_targets.py       # CLI for target management
run_scraper.py         # Main runner script
streamlit_app.py       # Price history dashboard
tests/                 # Test suite
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Disclaimer

This software is provided for educational purposes. Users are responsible for ensuring compliance with applicable laws, terms of service, and ethical guidelines when scraping websites.
