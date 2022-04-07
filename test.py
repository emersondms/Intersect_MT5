import MetaTrader5 as mt5
from jproperties import Properties
import backtest_excel 
import stocks_dataframe
import send_order
import position
import time

if not mt5.initialize():
    print("initialize() failed, error code = ", mt5.last_error())
    quit()

#============================================================================
# load properties file
props = Properties()

with open('order.properties', 'rb') as config_file:
    props.load(config_file)

#============================================================================
# calculate the number of positions to open
number_of_positions_to_open = int(props.get("NUMBER_OF_POSITIONS_TO_OPEN").data)
number_of_positions_opened = position.get_total_of_positions_opened(mt5)

print (f"\n{number_of_positions_opened} positions already opened")
if (number_of_positions_opened >= number_of_positions_to_open):    
    quit()

number_of_positions_to_open -= number_of_positions_opened
print (f"{number_of_positions_to_open} positions to open")

#============================================================================
stocks_dict = backtest_excel.get_stocks_dict(r"intersect_backtest.xlsx")
good_stocks_rates_df = stocks_dataframe.get_good_stocks_rates(mt5, stocks_dict)

# sort the dataframe to get the best stocks 
good_stocks_rates_df = good_stocks_rates_df.sort_values(
    by=['PROFIT_FACTOR', 'DIFF_FROM_CLOSE_TO_HALF'], ascending=False)

print ("\n",good_stocks_rates_df)

#============================================================================
# check if an already opened position is good for medium price
stocks_to_buy = []

for row in range(0, len(good_stocks_rates_df)):
    stock = good_stocks_rates_df.iloc[row].name
    if (position.get_position_lots(mt5, stock) > 0):
        stocks_to_buy.append(stock)

#============================================================================
# fill the stocks_to_buy array
row_index = 0

while not (len(stocks_to_buy) == number_of_positions_to_open):
    stock = good_stocks_rates_df.iloc[row_index].name
    if (not stock in stocks_to_buy):
        stocks_to_buy.append(stock)
    else:
        row_index += 1    

print (f"\nStocks to buy: {stocks_to_buy}")

#============================================================================
# buy the stocks
money_stake = float(props.get("MONEY_STAKE_FOR_EACH_POSITION").data)

for stock in stocks_to_buy:
    price = good_stocks_rates_df.loc[stock]['CLOSE']
    lots = position.calculate_lots_size(money_stake, price)
    send_order.buy_at_market(mt5, stock, lots)
    time.sleep(1)

mt5.shutdown()