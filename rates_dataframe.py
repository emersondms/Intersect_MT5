import warnings
import pandas as pd

warnings.filterwarnings("ignore")

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
    '''Returns today stocks rates from a stock list
    @param mt5_conn: MetaTrader5 connection object
    @param stocks_dict: a dictionary with <stock_name, profit_factor>
    @returns rates_df: a dataframe with the stocks information     
    '''
    rates_df = pd.DataFrame(columns=['OPEN', 'HIGH', 'LOW', 'CLOSE', 
        'PROFIT_FACTOR', 'DIFF_FROM_CLOSE_TO_HALF', 'DIFF_FROM_CLOSE_TO_LOW'])
    rates_df.set_index(rates_df.columns[0])

    for stock in stocks_dict.keys():
        try: 
            candle_info = mt5_conn.copy_rates_from_pos(
                stock, mt5_conn.TIMEFRAME_D1, 0,1) # 0,1 = today candle
            open = float(candle_info[0][1])
            high = float(candle_info[0][2])
            low = float(candle_info[0][3])
            close = float(candle_info[0][4])
            profit_factor = float(stocks_dict[stock])

            candle_half = round(((high + low) / 2), 2)
            diff_from_close_to_half = round((((candle_half - close) * 100) / candle_half), 1)
            diff_from_close_to_low = round((((close - low) * 100) / close), 1)

            rates_df.loc[stock] = [open, high, low, close, 
                profit_factor, diff_from_close_to_half, diff_from_close_to_low]
        except:
            continue
    return rates_df

#============================================================================
def get_good_stocks_rates(mt5_conn, stocks_dict):
    '''Returns the stocks that are matching with the strategy
    @param mt5_conn: MetaTrader5 connection object
    @param stocks_dict: a dictionary with <stock_name, profit_factor>
    @returns good_stocks_df: a dataframe with the filtered stocks     
    '''
    good_stocks_df = pd.DataFrame(columns=['OPEN', 'HIGH', 'LOW', 'CLOSE', 
        'PROFIT_FACTOR', 'DIFF_FROM_CLOSE_TO_HALF', 'DIFF_FROM_CLOSE_TO_LOW'])
    good_stocks_df.set_index(good_stocks_df.columns[0])
    all_stocks_df = get_today_stocks_rates(mt5_conn, stocks_dict)
    MAX_CANDLE_TAIL_SIZE = 0.3

    for stock in stocks_dict.keys():
        try:
            high = float(all_stocks_df.loc[stock]['HIGH'])
            low = float(all_stocks_df.loc[stock]['LOW'])
            close = float(all_stocks_df.loc[stock]['CLOSE'])
            open = float(all_stocks_df.loc[stock]['OPEN'])
            candle_size = high - low 

            # The stock matches the strategy if the closing price is near the low price
            strategy_matching = ((close - low) < (candle_size * 
                MAX_CANDLE_TAIL_SIZE)) and (close < open)
            if (strategy_matching): 
                good_stocks_df = good_stocks_df.append(all_stocks_df.loc[stock])
        except:
            continue
    return good_stocks_df


