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
logs.info(f">>> CLOSE POSITIONS")

def email_logs_and_quit():
    email_logs.send_email("[INTERSECT] CLOSE POSITIONS")
    quit()

# to not execute it on weekends
current_day_of_week = datetime_utils.get_current_day_of_week()
invalid_days = ["Saturday", "Sunday", "Monday"]
if (current_day_of_week in invalid_days):
    logs.error("Invalid date, exiting...")
    email_logs_and_quit()

if not mt5.initialize():
    logs.error("initialize() failed, error code = ", mt5.last_error())
    email_logs_and_quit()

#============================================================================
stocks_dict = backtest_data.get_stocks_dict()
stocks_with_opened_position = position.get_stocks_with_opened_position(mt5, stocks_dict)
stocks_to_close_position = []

def close_positions(stocks_list):
    logs.info(f"Closing positions: {stocks_list}")
    for stock in stocks_list:
        lots = position.get_position_lots(mt5, stock)
        send_order.sell_at_market(mt5, stock, lots)

#============================================================================
# close all positions on fridays
if (current_day_of_week == "Friday"):
    logs.info("Today is friday, closing all positions...")

    for stock in stocks_with_opened_position:
        stocks_to_close_position.append(stock)

    close_positions(stocks_to_close_position)
    email_logs_and_quit()

#============================================================================
# close positions that the closing is greater than half price
num_candles = 1 # today

for stock in stocks_with_opened_position:
    rates_df = rates_dataframe.get_stock_rates(mt5, stock, num_candles)
    today_rates = rates_df.iloc[0]

    today_high = float(today_rates['high'])
    today_low = float(today_rates['low'])
    today_close = float(today_rates['close'])
    today_half = round(((today_high + today_low) / 2), 2)

    if (today_close >= today_half):
        stocks_to_close_position.append(stock)

#============================================================================
# close positions opened 2 days ago
num_candles = 3 # before yesterday

# positions are not opened on weekends
if (current_day_of_week != "Monday") and (current_day_of_week != "Tuesday"):
    for stock in stocks_with_opened_position:
        rates_df = rates_dataframe.get_stock_rates(mt5, stock, num_candles)
        before_yesterday_open_date = datetime_utils.remove_time(rates_df.iloc[2]['time'])

        position_open_timestamp = position.get_position_open_timestamp(mt5, stock)
        position_open_datetime = datetime_utils.get_datetime_obj(position_open_timestamp)
        position_open_date = datetime_utils.remove_time(position_open_datetime)

        if (position_open_date == before_yesterday_open_date):
            if (not stock in stocks_to_close_position):
                stocks_to_close_position.append(stock)

#============================================================================
close_positions(stocks_to_close_position)
mt5.shutdown()
email_logs_and_quit()