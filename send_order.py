def buy_at_market(mt5_conn, stock, lots):
    '''Sends a buy at market order
    @param mt5_conn: MetaTrader5 connection object
    @param stock: name
    @param lots: size as double, ex: 100.0
    @returns: the request result object
    '''

    request = {
        "symbol": stock, 
        "volume": lots,
        "type": mt5_conn.ORDER_TYPE_BUY,
        "action": mt5_conn.TRADE_ACTION_DEAL, #at market
        "type_time": mt5_conn.ORDER_TIME_DAY,
        "type_filling": mt5_conn.ORDER_FILLING_RETURN
    }

    try:
        print(f"\n>>> BUY AT MARKET order sent: {request}")
        result = mt5_conn.order_send(request) 
        print(f"    RESULT: {result}")
        return result.order
    except:
        print(f"    FAILED: {mt5_conn.last_error()}")
    return ""

def sell_limit(mt5_conn, stock, lots, price):
    '''Sends a sell limit order
    @param mt5_conn: MetaTrader5 connection object
    @param stock: name
    @param lots: size as double, ex: 100.0
    @param price: sell price as float
    @returns: the request result object
    '''
    
    request = { 
        "symbol": stock, 
        "volume": lots,
        "price": price,
        "type": mt5_conn.ORDER_TYPE_SELL_LIMIT,
        "action": mt5_conn.TRADE_ACTION_PENDING,
        "type_time": mt5_conn.ORDER_TIME_DAY,
        "type_filling": mt5_conn.ORDER_FILLING_RETURN
    }

    try:
        print(f"\n>>> SELL LIMIT order sent: {request}")
        result = mt5_conn.order_send(request) 
        print(f"    RESULT: {result}")
        return result.order
    except:
        print(f"    FAILED: {mt5_conn.last_error()}")
    return ""

def sell_at_market(mt5_conn, stock, lots):
    '''Sends a sell at market order
    @param mt5_conn: MetaTrader5 connection object
    @param stock: name
    @param lots: size as double, ex: 100.0
    @returns: the request result object
    '''
    
    request = { 
        "symbol": stock, 
        "volume": lots,
        "type": mt5_conn.ORDER_TYPE_SELL,
        "action": mt5_conn.TRADE_ACTION_DEAL, #at market
        "type_time": mt5_conn.ORDER_TIME_DAY,
        "type_filling": mt5_conn.ORDER_FILLING_RETURN
    }

    try:
        print(f"\n>>> SELL AT MARKET order sent: {request}")
        result = mt5_conn.order_send(request) 
        print(f"    RESULT: {result}")
        return result.order
    except:
        print(f"    FAILED: {mt5_conn.last_error()}")
    return ""