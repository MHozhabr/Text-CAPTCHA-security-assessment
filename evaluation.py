import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

# Data sets
set1 = [238, 59.5, 208, 17.3, 27.7, 15.2, 78.1, 25.8, 51, 65.8]   # uppercase captcha
#set1 = [384.6, 625, 555.6, 588.2, 434.8, 666.7, 555.6, 555.6, 526.3, 588.2]   # equation captcha
set2 = [46.3, 158, 151, 8.3, 56.8, 37.3, 217, 208, 23.6, 212.7]   # 5 letter captcha
#set1= [113.6, 42.3, 175.4, 188.7, 188.7, 42, 140.8, 39.6, 156.3, 43.9]   # hybrid captcha

# Median
median1 = np.median(set1)
median2 = np.median(set2)

# Interquartile Range (IQR)
iqr1 = stats.iqr(set1)
iqr2 = stats.iqr(set2)

# Percentiles
percentiles1 = np.percentile(set1, [25, 50, 75, 90])
percentiles2 = np.percentile(set2, [25, 50, 75, 90])

# Display results
print("Set 1 Analysis:")
print(f"Median: {median1}")
print(f"IQR: {iqr1}")
print(f"Percentiles (25th, 50th, 75th, 90th): {percentiles1}")

print("Set 2 Analysis:")
print(f"Median: {median2}")
print(f"IQR: {iqr2}")
print(f"Percentiles (25th, 50th, 75th, 90th): {percentiles2}")

# Visualization
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12, 15))

# Box Plot
axes[0, 0].boxplot([set1, set2], tick_labels=['Set 1', 'Set 2'])
axes[0, 0].set_title('Box Plot Comparison')
axes[0, 0].set_ylabel('Values')

# Median
axes[0, 1].bar(['Set 1', 'Set 2'], [median1, median2], color=['blue', 'orange'])
axes[0, 1].set_title('Median Comparison')
axes[0, 1].set_ylabel('Median')
axes[0, 1].text(0, median1 + 2, f'{median1:.1f}', ha='center')
axes[0, 1].text(1, median2 + 3, f'{median2:.1f}', ha='center')

# IQR
axes[1, 0].bar(['Set 1', 'Set 2'], [iqr1, iqr2], color=['blue', 'orange'])
axes[1, 0].set_title('IQR Comparison')
axes[1, 0].set_ylabel('IQR')
axes[1, 0].text(0, iqr1 + 5, f'{iqr1:.1f}', ha='center')
axes[1, 0].text(1, iqr2 + 5, f'{iqr2:.1f}', ha='center')


# Percentiles
percentile_labels = ['25th', '50th', '75th', '90th']
x = np.arange(len(percentile_labels))

axes[1, 1].bar(x - 0.2, percentiles1, width=0.4, label='Set 1', color='blue')
axes[1, 1].bar(x + 0.2, percentiles2, width=0.4, label='Set 2', color='orange')
axes[1, 1].set_title('Percentiles Comparison')
axes[1, 1].set_xticks(x)
axes[1, 1].set_xticklabels(percentile_labels)
axes[1, 1].set_ylabel('Percentile Values')
axes[1, 1].legend()

for i, v in enumerate(percentiles1):
    axes[1, 1].text(i - 0.2, v + 2, f'{v:.1f}', ha='center')
for i, v in enumerate(percentiles2):
    axes[1, 1].text(i + 0.2, v + 2, f'{v:.1f}', ha='center')

plt.show()
