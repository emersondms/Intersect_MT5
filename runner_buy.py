from logger import logs
import datetime_utils
import MetaTrader5 as mt5
import email_logs
from jproperties import Properties
import backtest_excel 
import rates_dataframe
import send_order
import position

#============================================================================
logs.info("")
logs.info(f">>> BUY")

def email_logs_and_quit():
    email_logs.send_email("BUY", "")
    quit()

# avoid being exposed on weekends
if (datetime_utils.get_current_day_of_week() == "Friday"):
    logs.error("Today is friday, exiting...")
    email_logs_and_quit()

if not mt5.initialize():
    logs.error("initialize() failed, error code = ", mt5.last_error())
    email_logs_and_quit()

#============================================================================
# load properties file
props = Properties()

with open('request.properties', 'rb') as config_file:
    props.load(config_file)

#============================================================================
# calculate the number of positions to open
num_positions_to_open = int(props.get("NUMBER_OF_POSITIONS_TO_OPEN").data)
num_opened_positions = position.get_total_of_opened_positions(mt5)

logs.info(f"{num_opened_positions} positions already opened")
if (num_opened_positions >= num_positions_to_open):
    email_logs_and_quit()

num_positions_to_open -= num_opened_positions
logs.info(f"{num_positions_to_open} positions to open")

# to wait for the last seconds of negotiation period
datetime_utils.wait_for_time_to_be(16,54,30)

#============================================================================
stocks_dict = backtest_excel.get_stocks_dict()
good_stocks_rates_df = rates_dataframe.get_good_stocks_rates(mt5, stocks_dict)

# sort the dataframe to get the best stocks 
good_stocks_rates_df = good_stocks_rates_df.sort_values(
    by=['PROFIT_FACTOR', 'DIFF_FROM_CLOSE_TO_HALF'], ascending=False)

logs.info(f"\n{good_stocks_rates_df}")

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

while not (len(stocks_to_buy) == num_positions_to_open):
    stock = good_stocks_rates_df.iloc[row_index].name
    if (not stock in stocks_to_buy):
        stocks_to_buy.append(stock)
    else:
        row_index += 1    

logs.info(f"Stocks to buy: {stocks_to_buy}")

#============================================================================
# buy the stocks
money_stake = float(props.get("MONEY_STAKE_FOR_EACH_POSITION").data)

for stock in stocks_to_buy:
    closing_price = good_stocks_rates_df.loc[stock]['CLOSE']
    lots = position.calculate_lots_size(money_stake, closing_price)
    send_order.buy_at_market(mt5, stock, lots)

#============================================================================
mt5.shutdown()
email_logs_and_quit()