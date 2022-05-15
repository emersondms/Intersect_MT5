import warnings
import pandas as pd
from logger import logs

warnings.filterwarnings("ignore")
pd.set_option('display.max_columns', None)

def get_stock_rates(mt5_conn, stock, num_candles):
    '''Returns the stock rates for the given number of days
    @param mt5_conn: MetaTrader5 connection object
    @param stock: name
    @param num_candles: number of days as integer
    @returns rates_df: a dataframe with the stock rates for the period    
    '''
    rates = mt5_conn.copy_rates_from_pos(stock, mt5_conn.TIMEFRAME_D1, 0, num_candles)
    rates_df = pd.DataFrame(rates)

    # convert the timestamp to datetime format
    rates_df['time'] = pd.to_datetime(rates_df['time'], unit='s')
    rates_df = rates_df.sort_values('time', ascending=False)
    
    return rates_df

#============================================================================
def get_today_stocks_rates(mt5_conn, stocks_dict):
    '''Returns today's stocks rates for the given stocks list
    @param mt5_conn: MetaTrader5 connection object
    @param stocks_dict: a dictionary with <stock_name, profit_factor>
    @returns rates_df: a dataframe with the stocks information     
    '''
    rates_df = pd.DataFrame(columns=['OPEN', 'HIGH', 'LOW', 'CLOSE', 
        'PROFIT_FACTOR', 'PERC_DIFF_FROM_CLOSE_TO_HALF'])#, 'DIFF_FROM_CLOSE_TO_LOW'])
    rates_df.set_index(rates_df.columns[0])

    for stock in stocks_dict.keys():
        candle_info = mt5_conn.copy_rates_from_pos(
            stock, mt5_conn.TIMEFRAME_D1, 0,1) # 0,1 = today candle
        
        if (candle_info is None):
            logs.error(f"No data for {stock} - {mt5_conn.last_error()}")
            continue

        open = float(candle_info[0][1])
        high = float(candle_info[0][2])
        low = float(candle_info[0][3])
        close = float(candle_info[0][4])
        #profit_factor = round((float(stocks_dict[stock])), 1)
        profit_factor = int(float(stocks_dict[stock]))

        candle_half = round(((high + low) / 2), 2)
        #perc_diff_from_close_to_half = round((((candle_half - close) * 100) / candle_half), 1)
        perc_diff_from_close_to_half = int(((candle_half - close) * 100) / candle_half)
        #diff_from_close_to_low = round((((close - low) * 100) / close), 1)

        rates_df.loc[stock] = [open, high, low, close, 
            profit_factor, perc_diff_from_close_to_half]#, diff_from_close_to_low]

    return rates_df

#============================================================================
def get_good_stocks_rates(stocks_df):
    '''Returns the stocks that are matching with the strategy
    @param stocks_df: a dataframe already populated
    @returns good_stocks_df: a dataframe with the filtered stocks     
    '''
    good_stocks_df = pd.DataFrame(columns=['OPEN', 'HIGH', 'LOW', 'CLOSE', 
        'PROFIT_FACTOR', 'PERC_DIFF_FROM_CLOSE_TO_HALF'])#, 'DIFF_FROM_CLOSE_TO_LOW'])
    good_stocks_df.set_index(good_stocks_df.columns[0])

    for row in range(0, len(stocks_df)):
        try:
            stock_data = stocks_df.iloc[row]
            high = float(stock_data['HIGH'])
            low = float(stock_data['LOW'])
            close = float(stock_data['CLOSE'])
            candle_20_percent = (high - low) / 5

            # check if the closing price is near the low price
            strategy_matching = (close - low) < candle_20_percent
            if (strategy_matching): 
                good_stocks_df = good_stocks_df.append(stock_data)
        except:
            continue
        
    return good_stocks_df

#============================================================================
def get_perc_diff_from_half_to_low(high, low):
    candle_half = (high + low) / 2
    percent_diff_from_half_to_low = ((candle_half - low) * 100) / candle_half
    return percent_diff_from_half_to_low

def get_avg_of_perc_diff_from_half_to_low(rates_df, avg_period):
    total = 0
    for day in range(avg_period):
        high = rates_df.iloc[day]['high']
        low = rates_df.iloc[day]['low']
        total += get_perc_diff_from_half_to_low(high, low)
    
    avg = total / avg_period
    return avg 