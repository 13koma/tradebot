import pandas as pd
import sqlalchemy 
from binance.client import AsyncClient
from binance import BinanceSocketManager
import asyncio
import config


async def main():
	client = await AsyncClient.create(config.api_key, config.api_secret)
	bsm = BinanceSocketManager(client)
	socket = bsm.trade_socket('ETHUSDT')
	async with socket as tscm:
		while True:
			msg = await tscm.recv()
			frame = createframe(msg)
			frame.to_sql('ETHUSDT', engine, if_exists='append', index=False)
			print(createframe(msg))
			await client.close_connection()
	
	# 	while True:
	# 		await socket.__aenter__()
	# 		msg = await socket.recv()
	# 		frame = createframe(msg)
	# 		frame.to_sql('ETHUSDT', engine, if_exists='append', index=False)
	# 		print(frame)

def createframe(msg):
	df = pd.DataFrame([msg])
	df = df.loc[:,['s', 'E', 'p']]
	df.columns = ['symbol', 'Time', 'Price']
	df.Price = df.Price.astype(float)
	df.Time = pd.to_datetime(df.Time, unit='ms')
	return df

engine = sqlalchemy.create_engine('sqlite:///ETHUSDTstream.db')

result = createframe(asyncio.run(main()))
# print(result)

if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	loop.run_until_complete(main())
