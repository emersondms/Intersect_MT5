import MetaTrader5 as mt5
import backtest_excel 
import stocks_dataframe
import send_order
import time

if not mt5.initialize():
    print("initialize() failed, error code = ", mt5.last_error())
    quit()

stocks_dict = backtest_excel.get_stocks_dict(r"intersect_backtest.xlsx")
good_stocks_rates_df = stocks_dataframe.get_good_stocks_rates(mt5, stocks_dict)

# sort the dataframe to get the best stocks 
good_stocks_rates_df = good_stocks_rates_df.sort_values(
    by=['PROFIT_FACTOR', 'DIFF_FROM_CLOSE_TO_HALF'], ascending=False)


print (good_stocks_rates_df)
# print (good_stocks_df.loc['UNIP6'].name)

#send_order.buy(mt5, "OIBR3", 100.0)
#time.sleep(5)
# send_order.sell(mt5, "OIBR3", 100.0, 0.83)

#mt5.shutdown()
