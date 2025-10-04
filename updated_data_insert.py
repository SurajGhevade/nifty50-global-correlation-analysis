from common_imports import *
load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "port": os.getenv("DB_PORT", 5432),
}

TICKERS = {
    "NIFTY50": "^NSEI",
    "DOW": "^DJI",
    "NASDAQ": "^IXIC",
    "FTSE100": "^FTSE",
    "DAX": "^GDAXI",
    "CAC40": "^FCHI",
    "NIKKEI225": "^N225",
    "HANGSENG": "^HSI",
    "KOSPI": "^KS11",
    "SHANGHAI_SSE": "000001.SS",
    "CRUDE_OIL": "CL=F",
    "GOLD": "GC=F",
    "SILVER": "SI=F",
    "BTC": "BTC-USD",
    "ETH": "ETH-USD",
    "VIX_US": "^VIX",
    "VIX_INDIA": "^INDIAVIX",
    "gift_nifty":"^GIFT"
}

def fetch_data():
    records = []
    for name, ticker in TICKERS.items():
        try:
            data = yf.Ticker(ticker).history(period="20y", interval="1d")
            if data.empty:
                print(f"No data for {name} ({ticker})")
                continue

            for index, row in data.iterrows():
                adj_close = float(row["Adj Close"]) if "Adj Close" in row else float(row["Close"])
                trade_date = index.date()
                record = (
                    float(row["Close"]),
                    adj_close,
                    float(row["Close"]),
                    float(row["High"]),
                    float(row["Low"]),
                    float(row["Open"]),
                    int(row["Volume"]) if not row["Volume"] is None else None,
                    ticker,
                    name,
                    trade_date
                )
                records.append(record)

            print(f"Fetched {len(data)} rows for {name} ({ticker})")

        except Exception as e:
            print(f"Error fetching {name} ({ticker}): {e}")

    return records

def insert_data(records):
    if not records:
        print("No records to insert.")
        return

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    sql = """
        INSERT INTO global_indices
        (Price, Adj_Close, Close, High, Low, Open, Volume, Ticker, Name, trade_date)
        VALUES %s
        ON CONFLICT (Ticker, trade_date) DO NOTHING
    """
    try:
        execute_values(cur, sql, records)
        conn.commit()
        print(f"Inserted {len(records)} rows (skipped duplicates) into global_indices")
    except Exception as e:
        conn.rollback()
        print(f"Insert error: {e}")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    data = fetch_data()
    if data:
        insert_data(data)