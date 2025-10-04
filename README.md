# Nifty 50 Global Correlation Analysis

## Project Overview

This project investigates the statistical relationship between India’s Nifty 50 index and major global stock indices, commodities, volatility indices, and cryptocurrencies.

The primary objective is to understand whether global market movements—both closing and opening—affect the closing and opening behavior of Nifty 50. The analysis includes both static correlations (overall co-movement) and rolling correlations (time-varying relationships), helping us distinguish between short-term and long-term dependencies.

---

## Assets Analyzed

We studied 15+ global assets, spanning stock indices, commodities, volatility indices, and cryptocurrencies.

| Index / Ticker           | Country / Region | Time Zone            | Offset vs IST | Opens Before NSE? |
| ------------------------ | ---------------- | -------------------- | ------------- | ----------------- |
| NIFTY50 (^NSEI)          | India            | IST (UTC +5:30)      | 0 hrs         | Reference         |
| NIKKEI225 (^N225)        | Japan            | JST (UTC +9)         | +3.5 hrs      | Yes               |
| KOSPI (^KS11)            | South Korea      | KST (UTC +9)         | +3.5 hrs      | Yes               |
| SHANGHAI_SSE (000001.SS) | China            | CST (UTC +8)         | +2.5 hrs      | Yes               |
| HANGSENG (^HSI)          | Hong Kong        | HKT (UTC +8)         | +2.5 hrs      | Yes               |
| FTSE100 (^FTSE)          | UK               | GMT/BST (UTC 0/+1)   | –5.5 / –4.5   | No                |
| DAX (^GDAXI)             | Germany          | CET/CEST (UTC +1/+2) | –4.5 / –3.5   | No                |
| CAC40 (^FCHI)            | France           | CET/CEST             | –4.5 / –3.5   | No                |
| DOW (^DJI)               | US               | EST/EDT (UTC –5/–4)  | –10.5 / –9.5  | No                |
| NASDAQ (^IXIC)           | US               | EST/EDT              | –10.5 / –9.5  | No                |
| CRUDE_OIL (CL=F)         | US Futures       | CST/CDT (UTC –6/–5)  | –11.5 / –10.5 | No                |
| GOLD (GC=F)              | US COMEX         | EST/EDT              | –10.5 / –9.5  | No                |
| SILVER (SI=F)            | US COMEX         | EST/EDT              | –10.5 / –9.5  | No                |
| BTC-USD                  | Global / 24×7    | UTC                  | –5.5 hrs      | 24×7              |
| ETH-USD                  | Global / 24×7    | UTC                  | –5.5 hrs      | 24×7              |
| VIX_US (^VIX)            | US Volatility    | CST/CDT              | –11.5 / –10.5 | No                |
| VIX_INDIA (^INDIAVIX)    | India            | IST (UTC +5:30)      | 0 hrs         | Reference         |

---

## Key Findings

### 1. Nifty50 Closing vs. Global Closing Correlations

#### Correlation with Global Stock Indices

 Nifty50 shows a moderate positive correlation with most global stock indices.
 Strongest correlations: European markets – DAX (0.57) and FTSE100 (0.56).
 Asian peers: KOSPI (0.46), Hangseng (0.37), Nikkei225 (0.35).
 US indices weaker: Dow (0.28), Nasdaq (0.26).

#### Correlation with Volatility (Fear Indices)

 Strong negative correlation with India VIX (–0.53) – a textbook inverse fear-vs-market relationship.
 Weak negative correlation with US VIX (–0.20), showing Indian markets are more sensitive to domestic fear than US fear.

#### Correlation with Commodities

 Weak to negligible: Gold (0.09), Silver (0.12), Crude Oil (0.22).
 Reinforces Gold & Silver as diversifiers in portfolios.

#### Correlation with Cryptocurrencies

 Very low: BTC (0.11), ETH (0.14).
 Suggests crypto moves independently of Indian equities.

#### Other Interesting Relationships

 Regional blocs: US (Dow–Nasdaq = 0.83), Europe (DAX–CAC40 = 0.91).
 Precious metals: Gold–Silver strongly correlated (0.76).
 Crypto: BTC–ETH also strongly correlated (0.79).
 US Fear: Nasdaq–VIX_US strongly negative (–0.72).

Implications:

 Diversification possible via gold, silver, crypto.
 Hedging possible via India VIX.
 Nifty is more aligned with Europe/Asia than US markets.
<img width="1800" height="1400" alt="nifty_vs_all_close_heatmap" src="https://github.com/user-attachments/assets/19747d67-7885-4a5a-9a46-c251226cdaac" />

---

### 2. Nifty50 Opening vs. Global Closing Correlations

#### Correlation with Global Stock Indices

 At the open, Nifty50 is more influenced by US markets:

   Dow (0.46), Nasdaq (0.43).
 Correlation with Europe weaker: DAX (0.39), FTSE100 (0.38).
 Hangseng turns negative (–0.23), suggesting overnight divergence.

#### Correlation with Volatility

 India VIX (–0.20) weaker at open, showing fear develops intraday.
 US VIX (–0.37) stronger at open, reflecting overnight US sentiment.

#### Correlation with Commodities & Crypto

 Still minimal: Gold (0.04), Silver (0.11), BTC (0.20), ETH (0.22).
 Confirms their diversification role.

#### Other Observations

 US indices (Dow–Nasdaq) less cohesive at open (0.49 vs. 0.83 at close).
 24/7 assets (Gold–Silver, BTC–ETH) retain strong correlations.
 Nasdaq–VIX_US link weaker at open (–0.24 vs. –0.72 at close).

Implications:

 Timing matters: Nifty open reacts to US close; Nifty close aligns more with Europe.
 Overnight dynamics: Fear gauges (VIX) are less impactful at open than during the trading session.
 Traders should watch overnight US moves; investors should value gold/crypto for diversification.
<img width="1800" height="1400" alt="nifty_vs_all_heatmap_open" src="https://github.com/user-attachments/assets/53905319-2fba-45d0-bda2-ba5541a2fc6d" />

---

### 3. Rolling Correlation (Nifty50 vs. US VIX, 2018–2025)

 Rolling correlations reveal dynamic relationships instead of a static number.

#### Key Insights

 Consistently inverse: Nifty50 vs. US VIX correlation is almost always negative.
 Crisis periods: Strong dips (–0.6 or lower) during COVID-19 (2020) and early 2023.
 Calm periods: Correlation weakens, sometimes turning positive (2021, 2024, late 2025).

Implications:

 Long-term averages can be misleading; correlations shift with macro conditions.
 Hedging with volatility works best in crises but is less effective in stable periods.
 Indian markets are partly globalized but still retain independent domestic drivers.

---

## How to Use

1. Run the provided Python notebooks/scripts.
2. Outputs include:

    `all_closes.csv`, `all_returns.csv`
    `{group}_corr.csv` and `{group}_heatmap.png`
    Rolling correlation CSV + PNG files
3. Modify tickers/time zones for further research.

---

## Conclusion

 Global markets do impact Nifty 50, but correlations are moderate, unstable, and time-dependent.
 Domestic factors remain dominant in driving Indian equities.
 Gold, Silver, and Crypto remain reliable diversifiers.
 India VIX is a powerful hedge tool, while US VIX reflects global sentiment spillovers.

---

## Next Steps

 Expand to intraday data for finer insights.
 Use Granger causality tests for lead-lag relationships.
 Incorporate sentiment and news analysis in depth.
 Develop predictive models combining global + domestic indicators.

---

## Author

Developed by Suraj Ghevade
