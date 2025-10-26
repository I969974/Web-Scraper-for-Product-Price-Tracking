import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from scraper.db import DB

DB_PATH = os.getenv('DATABASE_PATH', 'data.db')

def main():
    st.title('Price Tracker')
    db = DB(DB_PATH)
    targets = db.list_targets()
    if not targets:
        st.info('No targets found. Add targets via the CLI or edit the database directly.')
        return
    for tid, url, name, target_price in targets:
        st.header(name or url)
        st.write(url)
        hist = db.get_price_history(tid)
        if not hist:
            st.write('No price history yet')
            continue
        df = pd.DataFrame(hist, columns=['ts', 'price'])
        df['ts'] = pd.to_datetime(df['ts'])
        st.line_chart(df.set_index('ts')['price'])
        st.write('Current:', df.iloc[-1]['price'])

if __name__ == '__main__':
    main()
