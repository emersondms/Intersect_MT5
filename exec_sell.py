import MetaTrader5 as mt5
import backtest_excel 
import rates_dataframe
import send_order
import position
import date_utils
import time

if not mt5.initialize():
    print("initialize() failed, error code = ", mt5.last_error())
    quit()

#============================================================================
stocks_dict = backtest_excel.get_stocks_dict(r"intersect_backtest.xlsx")
stocks_with_position_opened = position.get_stocks_with_position_opened(mt5, stocks_dict)

today_date = date_utils.remove_time(date_utils.get_today_date())
print (f"Today: {today_date}")

num_candles = 2 # today and yesterday

#============================================================================
# open sell orders on yesterday's half price
for stock in stocks_with_position_opened:
    rates_df = rates_dataframe.get_stock_rates(mt5, stock, num_candles)
    first_row_date = date_utils.remove_time(rates_df.iloc[0]['time'])
    yesterday_rates = rates_df.iloc[1]

    # in case today's candle is not available yet
    if (first_row_date != today_date):
        yesterday_rates = rates_df.iloc[0]

    # calculate sell price
    high = float(yesterday_rates['high'])
    low = float(yesterday_rates['low'])
    yesterday_half = round(((high + low) / 2), 2)

    lots = position.get_position_lots(mt5, stock)
    send_order.sell_limit(mt5, stock, lots, yesterday_half)
    time.sleep(1)
