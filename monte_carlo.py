import numpy as np
import matplotlib.pyplot as plt

initial_investment = 10000
time_horizon = 252
num_simulations = 10000
annual_return = 0.1245
annual_volatility = 0.1876

dt = 1 / 252
drift = (annual_return - 0.5 * annual_volatility ** 2) * dt
diffusion = annual_volatility * np.sqrt(dt)

np.random.seed(42)

all_simulations = np.zeros((num_simulations, time_horizon + 1))
all_simulations[:, 0] = initial_investment

for sim in range(num_simulations):
    price = initial_investment
    for day in range(1, time_horizon + 1):
        shock = np.random.normal(0, 1)
        price = price * np.exp(drift + diffusion * shock)
        all_simulations[sim, day] = price

final_values = all_simulations[:, -1]

mean_final = np.mean(final_values)
median_final = np.median(final_values)
std_final = np.std(final_values)
percentile_5 = np.percentile(final_values, 5)
percentile_95 = np.percentile(final_values, 95)
min_value = np.min(final_values)
max_value = np.max(final_values)

print(f"MONTE CARLO SIMULATION RESULTS")
print(f"Initial Investment: ${initial_investment:,.0f}")
print(f"Time Horizon: {time_horizon} days (1 year)")
print(f"Number of Simulations: {num_simulations:,}")
print(f"\nFINAL PORTFOLIO VALUE STATISTICS:")
print(f"Mean: ${mean_final:,.0f}")
print(f"Median: ${median_final:,.0f}")
print(f"Std Dev: ${std_final:,.0f}")
print(f"\n5th Percentile (Worst 5%): ${percentile_5:,.0f}")
print(f"95th Percentile (Best 5%): ${percentile_95:,.0f}")
print(f"\nWorst Case: ${min_value:,.0f}")
print(f"Best Case: ${max_value:,.0f}")
print(f"\nProbability of Profit: {100 * np.sum(final_values > initial_investment) / num_simulations:.1f}%")

fig, axes = plt.subplots(2, 2, figsize=(16, 10))

for i in range(100):
    axes[0, 0].plot(all_simulations[i], alpha=0.3, linewidth=0.5)
axes[0, 0].axhline(initial_investment, color='red', linestyle='--', linewidth=2, label='Initial Investment')
axes[0, 0].set_title(f'Sample of 100 Simulated Price Paths', fontsize=14, fontweight='bold')
axes[0, 0].set_xlabel('Trading Day')
axes[0, 0].set_ylabel('Portfolio Value ($)')
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

axes[0, 1].hist(final_values, bins=50, color='blue', alpha=0.7, edgecolor='black')
axes[0, 1].axvline(initial_investment, color='red', linestyle='--', linewidth=2, label='Initial Investment')
axes[0, 1].axvline(mean_final, color='green', linestyle='--', linewidth=2, label=f'Mean: ${mean_final:,.0f}')
axes[0, 1].axvline(median_final, color='orange', linestyle='--', linewidth=2, label=f'Median: ${median_final:,.0f}')
axes[0, 1].set_title('Distribution of Final Portfolio Values', fontsize=14, fontweight='bold')
axes[0, 1].set_xlabel('Final Portfolio Value ($)')
axes[0, 1].set_ylabel('Frequency')
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

percentiles = np.percentile(all_simulations, [5, 25, 50, 75, 95], axis=0)
days = np.arange(time_horizon + 1)
axes[1, 0].fill_between(days, percentiles[0], percentiles[4], alpha=0.3, label='5th-95th percentile')
axes[1, 0].fill_between(days, percentiles[1], percentiles[3], alpha=0.5, label='25th-75th percentile')
axes[1, 0].plot(days, percentiles[2], color='red', linewidth=2, label='Median')
axes[1, 0].axhline(initial_investment, color='black', linestyle='--', linewidth=1, label='Initial Investment')
axes[1, 0].set_title('Portfolio Value Confidence Intervals', fontsize=14, fontweight='bold')
axes[1, 0].set_xlabel('Trading Day')
axes[1, 0].set_ylabel('Portfolio Value ($)')
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3)

returns = (final_values - initial_investment) / initial_investment * 100
axes[1, 1].hist(returns, bins=50, color='purple', alpha=0.7, edgecolor='black')
axes[1, 1].axvline(0, color='red', linestyle='--', linewidth=2, label='Break-even')
axes[1, 1].axvline(np.mean(returns), color='green', linestyle='--', linewidth=2, label=f'Mean: {np.mean(returns):.1f}%')
axes[1, 1].set_title('Distribution of Returns (%)', fontsize=14, fontweight='bold')
axes[1, 1].set_xlabel('Return (%)')
axes[1, 1].set_ylabel('Frequency')
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('monte_carlo_simulation.png', dpi=150, bbox_inches='tight')
plt.show()

print("\nSimulation complete! Chart saved as 'monte_carlo_simulation.png'")