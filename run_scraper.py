import os
import time
import argparse
from dotenv import load_dotenv
from scraper.scraper import Scraper

# Load environment from .env if present
load_dotenv()


def main(run_once: bool = False, interval_minutes: int = 60):
    s = Scraper()
    if run_once:
        s.check_all()
        return
    try:
        while True:
            print("Running check...")
            s.check_all()
            print(f"Sleeping {interval_minutes} minutes...")
            time.sleep(interval_minutes * 60)
    except KeyboardInterrupt:
        print("Stopped")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--once", action='store_true')
    parser.add_argument("--interval", type=int, default=int(os.getenv('CHECK_INTERVAL_MINUTES', '60')))
    args = parser.parse_args()
    main(run_once=args.once, interval_minutes=args.interval)
