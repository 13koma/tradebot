import sqlalchemy
import pandas as pd
from binance.client import Client
import config
import matplotlib.pyplot as plt

# df = pd.read_sql('ETHUSDT', engine)

# df.Price.plot()

#Trendfollowing
#if the crypto was raising by x % -> Buy
#exit when profit is above 0.15% or loss is crossing -0.15%

def strategy(entry, lookback, qty, open_position=False):
	client = Client(config.api_key, config.api_secret)
	engine = sqlalchemy.create_engine('sqlite:///ETHUSDTstream.db')
	while True:
		df = pd.read_sql('ETHUSDT', engine)
		lookbackperiod = df.iloc[-lookback:]
		cumret = (lookbackperiod.Price.pct_change() +1).cumprod() - 1
		if not open_position:
			if cumret[cumret.last_valid_index()] > entry:
				order = client.create_order(symbol='ETHUSDT',
											side='BUY',
											type='MARKET',
											quantity=qty)
				print(order)
				open_position = True
				break
	if open_position:
		while True:
			df = pd.read_sql('ETHUSDT', engine)
			sincebuy = df.loc[df.Time > 
							  pd.to_datetime(order['transactTime'],
							  unit='ms')]
			if len(sincebuy) > 1:
				sincebuyret = (sincebuy.Price.pct_change() + 1).cumprod - 1
				last_entry = sincebuyret[sincebuyret.last_valid_index()]
				if last_entry > 0.0015 or last_entry < -0.0015:
					order = client.create_order(symbol='ETHUSDT',
												side='SELL',
												type='MARKET',
												quantity=qty)
					print(order)
					break

strategy(0.01, 60, 0.001)





# plt.show()

