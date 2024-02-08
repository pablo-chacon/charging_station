import requests as r
import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
#import seaborn as sns
import warnings 
warnings.filterwarnings('ignore')
# Plotting the price per hour and the consumption per hour.


price_data = r.get("http://127.0.0.1:5000/priceperhour").json()
consumption_data = r.get("http://127.0.0.1:5000/baseload").json()
price_hour = range(0, len(price_data))
price_data = pd.DataFrame(price_data)
consumption_data = pd.DataFrame(consumption_data)
price_data.head()
fig, axs = plt.subplots()
axs.plot(price_hour, price_data)
axs.plot(price_hour, consumption_data)
fig.suptitle('Pricing and Consumption')