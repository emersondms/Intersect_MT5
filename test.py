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

#print (good_stocks_rates_df)
# print (good_stocks_df.loc['UNIP6'].name)
#print(good_stocks_rates_df.iloc[0].name,"\n")


positions=mt5.positions_get(symbol="MGLU3")
if positions==None:
    print("No positions on MGLU3, error code={}".format(mt5.last_error()))
elif len(positions)>0:
    print("Total positions on MGLU3 =",len(positions))
    print(positions)
else: 
    print("No positions on MGLU3")






'''
lots = 100.0
stock = "MGLU3"
sell_price = 7.15


send_order.buy_at_market(mt5, stock, lots)
time.sleep(5)
send_order.sell_limit(mt5, stock, lots, sell_price)
#mt5.shutdown()
'''