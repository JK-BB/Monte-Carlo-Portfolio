import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

ticker = yf.Ticker("SPY")
data = ticker.history(period="5y")

print(f"Downloaded {len(data)} days of data")
print(f"Date range: {data.index[0].date()} to {data.index[-1].date()}")
print("\nFirst 5 rows:")
print(data[['Open', 'High', 'Low', 'Close', 'Volume']].head())

prices = data['Close']
daily_returns = prices.pct_change().dropna()

print(f"\nCalculated {len(daily_returns)} daily returns")
print("\nFirst 5 daily returns:")
for i in range(5):
    date = daily_returns.index[i].date()
    ret = daily_returns.iloc[i]
    print(f"  {date}: {ret:.6f} = {ret*100:.4f}%")

mean_daily_return = daily_returns.mean()
annual_return = mean_daily_return * 252

print(f"\nMean daily return: {mean_daily_return:.6f}")
print(f"Annual return (μ): {annual_return:.4f} ({annual_return*100:.2f}%)")

daily_volatility = daily_returns.std()
annual_volatility = daily_volatility * np.sqrt(252)

print(f"\nDaily volatility: {daily_volatility:.6f}")
print(f"Annual volatility (σ): {annual_volatility:.4f} ({annual_volatility*100:.2f}%)")

print(f"\nSUMMARY:")
print(f"Drift (μ): {annual_return:.4f} ({annual_return*100:.2f}%)")
print(f"Volatility (σ): {annual_volatility:.4f} ({annual_volatility*100:.2f}%)")

fig, axes = plt.subplots(2, 1, figsize=(12, 8))

axes[0].plot(prices.index, prices.values, linewidth=2, color='blue')
axes[0].set_title('SPY Historical Prices (Last 5 Years)', fontsize=14, fontweight='bold')
axes[0].set_xlabel('Date')
axes[0].set_ylabel('Price ($)')
axes[0].grid(True, alpha=0.3)

axes[1].hist(daily_returns, bins=50, color='green', alpha=0.7, edgecolor='black')
axes[1].axvline(mean_daily_return, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_daily_return:.6f}')
axes[1].set_title('Distribution of Daily Returns', fontsize=14, fontweight='bold')
axes[1].set_xlabel('Daily Return')
axes[1].set_ylabel('Frequency')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('spy_analysis.png', dpi=150, bbox_inches='tight')
plt.show()