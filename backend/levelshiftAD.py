import pandas as pd
from adtk.data import validate_series
from adtk.detector import LevelShiftAD
import matplotlib.pyplot as plt

s = pd.read_csv("./uploads/dataset.csv", index_col="Datetime", parse_dates=True)
s = validate_series(s)

level_shift_ad = LevelShiftAD(c=2.0, side='both', window=35)
anomalies = level_shift_ad.fit_detect(s)

anomaly_flags = anomalies.iloc[:, 0].fillna(False)  # Convert NaN to False
anomaly_dates = anomalies.index[anomaly_flags]  # Clean boolean series for indexing

plt.figure(figsize=(12, 6))

plt.plot(s, label='Time Series', linewidth=1)

plt.vlines(anomaly_dates, ymin=s.min(), ymax=s.max(), colors='red', label='Anomalies')

plt.legend()
plt.xlabel('Datetime')
plt.ylabel('CPU Consumption')
plt.title('LevelShiftAd Detection Result')
plt.savefig('plot.png', dpi=300)
plt.close()