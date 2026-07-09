import csv
import argparse
import sqlite3

CSV_FILE = "data/octanove-vocabulary-profile-c1c2-1.0.csv"
TXT_FILE = "words.txt"
DB_FILE = "vocab.db"


def create_words_table(cur):
    cur.execute("""
    CREATE TABLE IF NOT EXISTS words (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        headword TEXT NOT NULL UNIQUE,
        cefr TEXT,
        definition TEXT
    )
    """)


def insert_rows(cur, rows):
    before = cur.connection.total_changes
    cur.executemany("""
        INSERT OR IGNORE INTO words (headword, cefr, definition)
        VALUES (?, ?, ?)
    """, rows)
    return cur.connection.total_changes - before


def import_csv(cur, csv_file):
    rows = []
    with open(csv_file, newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        for row in reader:
            headword = row["headword"].strip()
            cefr = row["CEFR"].strip()

            if not headword:
                continue

            rows.append((headword, cefr, None))

    inserted = insert_rows(cur, rows)
    return len(rows), inserted


def import_txt(cur, txt_file):
    rows = []
    seen = set()
    with open(txt_file, encoding="utf-8-sig") as file:
        for line in file:
            headword = line.strip()

            if not headword or headword in seen:
                continue

            seen.add(headword)
            rows.append((headword, None, None))

    inserted = insert_rows(cur, rows)
    return len(rows), inserted


def parse_args():
    parser = argparse.ArgumentParser(
        description="Import vocabulary words into the SQLite database."
    )
    parser.add_argument(
        "--source",
        choices=("csv", "txt"),
        default="csv",
        help="Input format to import. Defaults to csv.",
    )
    parser.add_argument(
        "--file",
        help=f"Input file path. Defaults to {CSV_FILE} for csv or {TXT_FILE} for txt.",
    )
    parser.add_argument(
        "--db",
        default=DB_FILE,
        help=f"SQLite database path. Defaults to {DB_FILE}.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    input_file = args.file or (TXT_FILE if args.source == "txt" else CSV_FILE)

    conn = sqlite3.connect(args.db)
    cur = conn.cursor()

    create_words_table(cur)

    if args.source == "txt":
        processed, inserted = import_txt(cur, input_file)
    else:
        processed, inserted = import_csv(cur, input_file)

    conn.commit()
    conn.close()

    print(
        f"Processed {processed} words from {input_file}; "
        f"inserted {inserted} new words into {args.db}"
    )


if __name__ == "__main__":
    main()
