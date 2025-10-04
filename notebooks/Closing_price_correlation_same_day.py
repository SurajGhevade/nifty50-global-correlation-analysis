from common_import import *
load_dotenv()
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "port": os.getenv("DB_PORT", 5432),
}
DB_URL = f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"
engine = create_engine(DB_URL)

BASE_DIR = "E:\\Financial_modeling\\Datascript\\Financial_market_corelation_project"
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
LOG_DIR = os.path.join(BASE_DIR, "logs")

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

GROUPS = {
    "nifty_vs_us": ["NIFTY50", "DOW", "NASDAQ"],
    "nifty_vs_europe": ["NIFTY50", "FTSE100", "DAX", "CAC40"],
    "nifty_vs_asia": ["NIFTY50", "NIKKEI225", "HANGSENG", "KOSPI", "SHANGHAI_SSE"],
    "nifty_vs_crude": ["NIFTY50", "CRUDE_OIL"],
    "nifty_vs_metals": ["NIFTY50", "GOLD", "SILVER"],
    "nifty_vs_crypto": ["NIFTY50", "BTC", "ETH"],
    "nifty_vs_vix": ["NIFTY50", "VIX_US", "VIX_INDIA"],
    "nifty_vs_all": ["NIFTY50", "VIX_US", "VIX_INDIA", "BTC", "ETH", "GOLD", "SILVER", 
                     "CRUDE_OIL", "DOW", "NASDAQ", "FTSE100", "DAX", "CAC40", "NIKKEI225", "HANGSENG", "KOSPI", "SHANGHAI_SSE"]
}

def fetch_from_db(start_date="2017-11-10"):
    conn = psycopg2.connect(**DB_CONFIG)
    query = f"SELECT trade_date, name, adj_close FROM global_indices WHERE trade_date >= '{start_date}';"
    df = pd.read_sql(query, engine)
    conn.close()
    df = df.pivot(index='trade_date', columns='name', values='adj_close')
    return df

def compute_returns(close_df):
    close_df = close_df.ffill().dropna(how='all')
    safe_df = close_df.replace(0, np.nan)
    returns = np.log(safe_df / safe_df.shift(1))
    returns = returns.dropna(how='all', axis=1)
    return returns

def correlation_matrix(returns_df, method='pearson'):
    return returns_df.corr(method=method)

def plot_heatmap(corr_df, outpath, title=None, big=False):
    plt.figure(figsize=(18,14) if big else (12,10))
    sns.heatmap(corr_df, annot=True, fmt=".2f", vmin=-1, vmax=1, square=True, cbar_kws={"shrink":0.8})
    if title: plt.title(title)
    plt.tight_layout()
    plt.savefig(outpath)
    plt.close()

def save_corr_and_plot(name, returns_df):
    corr = correlation_matrix(returns_df)
    csv_path = os.path.join(OUTPUT_DIR, f"{name}_corr.csv")
    png_path = os.path.join(OUTPUT_DIR, f"{name}_heatmap.png")
    corr.to_csv(csv_path)
    plot_heatmap(corr, png_path, title=f"Correlation: {name}", big=(name=='nifty_vs_all'))
    # print(f"Saved CSV: {csv_path}")
    # print(f"Saved PNG: {png_path}")

def rolling_correlation(series_a, series_b, window=60):
    return series_a.rolling(window).corr(series_b)

def save_rolling_corr(series_a, series_b, name_a, name_b):
    rc = rolling_correlation(series_a, series_b)
    rc_csv = os.path.join(OUTPUT_DIR, f"rolling_corr_{name_a}_{name_b}.csv")
    rc_png = os.path.join(OUTPUT_DIR, f"rolling_corr_{name_a}_{name_b}.png")
    rc.to_csv(rc_csv)
    plt.figure(figsize=(12,4))
    plt.plot(rc)
    plt.title(f"60-day rolling correlation: {name_a} vs {name_b}")
    plt.xlabel("Date")
    plt.ylabel("Rolling Corr")
    plt.tight_layout()
    plt.savefig(rc_png)
    plt.close()
    # print(f"Saved rolling correlation: {rc_csv}, {rc_png} \n")

def run_analysis(start_date="2017-11-10"):
    close_df = fetch_from_db(start_date=start_date)
    close_df.to_csv(os.path.join(OUTPUT_DIR, "all_closes.csv"))
    # print("Saved all_closes.csv \n")

    returns = compute_returns(close_df)
    returns.to_csv(os.path.join(OUTPUT_DIR, "all_returns.csv"))
    # print("Saved all_returns.csv \n")

    for group_name, tickers in GROUPS.items():
        tickers_exist = [t for t in tickers if t in returns.columns]
        if len(tickers_exist) < 2:
            print(f"Skipping group {group_name}, not enough data")
            continue
        save_corr_and_plot(group_name, returns[tickers_exist])

        for t in tickers_exist:
            if t == "nifty50": 
                continue
            save_rolling_corr(returns["nifty50"], returns[t], "nifty50", t)


if __name__ == "__main__":
    run_analysis(start_date="2020-11-10")