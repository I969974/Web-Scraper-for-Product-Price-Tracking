#!/usr/bin/env python3
import argparse
from dotenv import load_dotenv
from scraper.db import DB
import os

load_dotenv()
DB_PATH = os.getenv('DATABASE_PATH', 'data.db')

def main():
    parser = argparse.ArgumentParser(description='Manage price tracker targets')
    sub = parser.add_subparsers(dest='cmd')

    p_add = sub.add_parser('add')
    p_add.add_argument('url')
    p_add.add_argument('--name')
    p_add.add_argument('--target', type=float)

    p_list = sub.add_parser('list')

    p_remove = sub.add_parser('remove')
    p_remove.add_argument('id', type=int)

    args = parser.parse_args()
    db = DB(DB_PATH)
    if args.cmd == 'add':
        tid = db.add_target(args.url, args.name, args.target)
        print('Added target id', tid)
    elif args.cmd == 'list':
        for tid, url, name, target in db.list_targets():
            print(tid, url, name, target)
    elif args.cmd == 'remove':
        # simple remove
        import sqlite3
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute('DELETE FROM targets WHERE id = ?', (args.id,))
        conn.commit()
        print('Removed', args.id)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
