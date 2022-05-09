from logger import logs
import MetaTrader5 as mt5
import email_logs
import backtest_data 
import rates_dataframe
import send_order
import position
import datetime_utils

#============================================================================
logs.info("")
logs.info(f">>> TAKE PROFIT")

def email_logs_and_quit():
    email_logs.send_email("[INTERSECT] TAKE PROFIT")
    quit()

# to not execute it on weekends
today = datetime_utils.get_current_day_of_week()
invalid_days = ["Saturday", "Sunday", "Monday"]
if (today in invalid_days):
    logs.error("Invalid day, exiting...")
    email_logs_and_quit()

if not mt5.initialize():
    logs.error("initialize() failed, error code = ", mt5.last_error())
    email_logs_and_quit()   

#============================================================================
# calcutate the target price and then open sell orders

stocks_dict = backtest_data.get_stocks_dict()
stocks_with_position_opened = position.get_stocks_with_opened_position(mt5, stocks_dict)
logs.info(f"Positions opened: {stocks_with_position_opened}")

today_date = datetime_utils.remove_time(datetime_utils.get_today_datetime())
num_candles = 20

for stock in stocks_with_position_opened:
    rates_df = rates_dataframe.get_stock_rates(mt5, stock, num_candles)
    first_row_date = datetime_utils.remove_time(rates_df.iloc[0]['time'])
    yesterday_rates = rates_df.iloc[1]

    # in case today's candle is not available yet
    if (first_row_date != today_date):
        yesterday_rates = rates_df.iloc[0]
    
    yesterday_high = float(yesterday_rates['high'])
    yesterday_low = float(yesterday_rates['low'])
    yesterday_close = float(yesterday_rates['close'])
    yesterday_half = round(((yesterday_high + yesterday_low) / 2), 2)

    # calculate the target sell price based on stock volatility  
    target_price = yesterday_close * 1.01
    avg_diff_from_half_to_low = rates_dataframe.get_avg_of_percent_diff_from_half_to_low(
        rates_df, num_candles)
        
    if (avg_diff_from_half_to_low < 1): 
        target_price = yesterday_close * 1.005  

    if (yesterday_half <= target_price): 
        target_price = yesterday_half

    logs.info(f"{stock} profit at: {target_price}")
    lots = position.get_position_lots(mt5, stock)
    send_order.sell_limit(mt5, stock, lots, target_price)

#============================================================================
mt5.shutdown()
email_logs_and_quit()