from common_import import *
load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "port": os.getenv("DB_PORT", 5432),
}
DB_URL = f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"
engine = create_engine(DB_URL)


BASE_DIR = r"E:\Financial_modeling\Datascript\Financial_market_corelation_project"
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def fetch_from_db(start_date="2017-11-10"):
    query = f"""
    WITH 
    NIFTY50 AS (
        SELECT trade_date, open as adj_close, name 
        FROM global_indices WHERE name = 'NIFTY50' ORDER BY trade_date
    ),
    DOW AS (
        SELECT trade_date, lag(adj_close) OVER (PARTITION BY name ORDER BY trade_date) AS adj_close, name 
        FROM global_indices WHERE name = 'DOW' ORDER BY trade_date
    ),
    ETH AS (
        SELECT trade_date, lag(adj_close) OVER (PARTITION BY name ORDER BY trade_date) AS adj_close, name 
        FROM global_indices WHERE name = 'ETH' ORDER BY trade_date
    ),
    GOLD AS (
        SELECT trade_date, lag(adj_close) OVER (PARTITION BY name ORDER BY trade_date) AS adj_close, name 
        FROM global_indices WHERE name = 'GOLD' ORDER BY trade_date
    ),
    CAC40 AS (
        SELECT trade_date, lag(adj_close) OVER (PARTITION BY name ORDER BY trade_date) AS adj_close, name 
        FROM global_indices WHERE name = 'CAC40' ORDER BY trade_date
    ),
    VIX_INDIA AS (
        SELECT trade_date, adj_close, name FROM global_indices WHERE name = 'VIX_INDIA' ORDER BY trade_date
    ),
    SILVER AS (
        SELECT trade_date, lag(adj_close) OVER (PARTITION BY name ORDER BY trade_date) AS adj_close, name 
        FROM global_indices WHERE name = 'SILVER' ORDER BY trade_date
    ),
    NIKKEI225 AS (
        SELECT trade_date, adj_close, name FROM global_indices WHERE name = 'NIKKEI225' ORDER BY trade_date
    ),
    HANGSENG AS (
        SELECT trade_date, adj_close, name FROM global_indices WHERE name = 'HANGSENG' ORDER BY trade_date
    ),
    SHANGHAI_SSE AS (
        SELECT trade_date, adj_close, name FROM global_indices WHERE name = 'SHANGHAI_SSE' ORDER BY trade_date
    ),
    DAX AS (
        SELECT trade_date, lag(adj_close) OVER (PARTITION BY name ORDER BY trade_date) AS adj_close, name 
        FROM global_indices WHERE name = 'DAX' ORDER BY trade_date
    ),
    NASDAQ AS (
        SELECT trade_date, lag(adj_close) OVER (PARTITION BY name ORDER BY trade_date) AS adj_close, name 
        FROM global_indices WHERE name = 'NASDAQ' ORDER BY trade_date
    ),
    BTC AS (
        SELECT trade_date, lag(adj_close) OVER (PARTITION BY name ORDER BY trade_date) AS adj_close, name 
        FROM global_indices WHERE name = 'BTC' ORDER BY trade_date
    ),
    FTSE100 AS (
        SELECT trade_date, lag(adj_close) OVER (PARTITION BY name ORDER BY trade_date) AS adj_close, name 
        FROM global_indices WHERE name = 'FTSE100' ORDER BY trade_date
    ),
    VIX_US AS (
        SELECT trade_date, lag(adj_close) OVER (PARTITION BY name ORDER BY trade_date) AS adj_close, name 
        FROM global_indices WHERE name = 'VIX_US' ORDER BY trade_date
    ),
    CRUDE_OIL AS (
        SELECT trade_date, lag(adj_close) OVER (PARTITION BY name ORDER BY trade_date) AS adj_close, name 
        FROM global_indices WHERE name = 'CRUDE_OIL' ORDER BY trade_date
    ),
    KOSPI AS (
        SELECT trade_date, adj_close, name FROM global_indices WHERE name = 'KOSPI' ORDER BY trade_date
    )
    SELECT 
        ns.trade_date,
        ns.adj_close AS NIFTY50,
        dow.adj_close AS DOW,
        eth.adj_close AS ETH,
        gold.adj_close AS GOLD,
        cac40.adj_close AS CAC40,
        vixi.adj_close AS VIX_INDIA,
        silver.adj_close AS SILVER,
        nikkei.adj_close AS NIKKEI225,
        hsi.adj_close AS HANGSENG,
        shanghai.adj_close AS SHANGHAI_SSE,
        dax.adj_close AS DAX,
        nasdaq.adj_close AS NASDAQ,
        btc.adj_close AS BTC,
        ftse.adj_close AS FTSE100,
        vixus.adj_close AS VIX_US,
        crude.adj_close AS CRUDE_OIL,
        kospi.adj_close AS KOSPI
    FROM NIFTY50 ns
    LEFT JOIN DOW dow ON dow.trade_date = ns.trade_date
    LEFT JOIN ETH eth ON eth.trade_date = ns.trade_date
    LEFT JOIN GOLD gold ON gold.trade_date = ns.trade_date
    LEFT JOIN CAC40 cac40 ON cac40.trade_date = ns.trade_date
    LEFT JOIN VIX_INDIA vixi ON vixi.trade_date = ns.trade_date
    LEFT JOIN SILVER silver ON silver.trade_date = ns.trade_date
    LEFT JOIN NIKKEI225 nikkei ON nikkei.trade_date = ns.trade_date
    LEFT JOIN HANGSENG hsi ON hsi.trade_date = ns.trade_date
    LEFT JOIN SHANGHAI_SSE shanghai ON shanghai.trade_date = ns.trade_date
    LEFT JOIN DAX dax ON dax.trade_date = ns.trade_date
    LEFT JOIN NASDAQ nasdaq ON nasdaq.trade_date = ns.trade_date
    LEFT JOIN BTC btc ON btc.trade_date = ns.trade_date
    LEFT JOIN FTSE100 ftse ON ftse.trade_date = ns.trade_date
    LEFT JOIN VIX_US vixus ON vixus.trade_date = ns.trade_date
    LEFT JOIN CRUDE_OIL crude ON crude.trade_date = ns.trade_date
    LEFT JOIN KOSPI kospi ON kospi.trade_date = ns.trade_date
    WHERE ns.trade_date >= '{start_date}'
    ORDER BY ns.trade_date;
    """
    df = pd.read_sql(query, engine)
    df = df.set_index('trade_date')
    logging.info(f"Fetched {len(df)} rows from DB")
    return df

def compute_returns(close_df):
    close_df = close_df.ffill().dropna(how='all')
    returns_df = np.log(close_df / close_df.shift(1))
    returns_df = returns_df.dropna(how='all', axis=1)
    return returns_df

def correlation_matrix(returns_df):
    return returns_df.corr()

def plot_heatmap(corr_df, outpath, title=None, big=False):
    plt.figure(figsize=(18,14) if big else (12,10))
    sns.heatmap(corr_df, annot=True, fmt=".2f", vmin=-1, vmax=1, square=True, cbar_kws={"shrink":0.8})
    if title: plt.title(title)
    plt.tight_layout()
    plt.savefig(outpath)
    plt.close()

def save_corr_and_plot(name, returns_df):
    corr = correlation_matrix(returns_df)
    csv_file = os.path.join(OUTPUT_DIR, f"{name}_corr_open.csv")
    png_file = os.path.join(OUTPUT_DIR, f"{name}_heatmap_open.png")
    corr.to_csv(csv_file)
    plot_heatmap(corr, png_file, title=f"Correlation: {name}", big=(name=="nifty_vs_all"))
    logging.info(f"Saved correlation CSV and heatmap for {name}")

def rolling_correlation(series_a, series_b, window=60):
    return series_a.rolling(window).corr(series_b)

def save_rolling_corr(series_a, series_b, name_a, name_b):
    rc = rolling_correlation(series_a, series_b)
    rc_csv = os.path.join(OUTPUT_DIR, f"rolling_corr_{name_a}_{name_b}_open.csv")
    rc_png = os.path.join(OUTPUT_DIR, f"rolling_corr_{name_a}_{name_b}_open.png")
    rc.to_csv(rc_csv)
    plt.figure(figsize=(12,4))
    plt.plot(rc)
    plt.title(f"Rolling correlation: {name_a} vs {name_b}")
    plt.savefig(rc_png)
    plt.close()
    logging.info(f"Saved rolling correlation for {name_a} vs {name_b}")

def run_analysis(start_date="2017-11-10"):
    close_df = fetch_from_db(start_date=start_date)
    close_file = os.path.join(OUTPUT_DIR, "all_closes_and_nifty_50_open.csv")
    close_df.to_csv(close_file)
    logging.info(f"Saved closes: {close_file}")

    returns_df = compute_returns(close_df)
    returns_file = os.path.join(OUTPUT_DIR, "all_closes_and_nifty_50_open_returns.csv")
    returns_df.to_csv(returns_file)
    logging.info(f"Saved returns: {returns_file}")

    GROUPS = {
        "nifty_vs_all": close_df.columns.tolist()
    }
    for name, tickers in GROUPS.items():
        tickers_exist = [t for t in tickers if t in returns_df.columns]
        if len(tickers_exist) < 2:
            continue
        save_corr_and_plot(name, returns_df[tickers_exist])

        for t in tickers_exist:
            if t == "nifty50":
                continue
            save_rolling_corr(returns_df["nifty50"], returns_df[t], "nifty50", t)

if __name__ == "__main__":
    run_analysis(start_date="2017-11-10")