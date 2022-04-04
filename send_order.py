def buy_at_market(mt5, stock, lots):
    request = {
        "symbol": stock, 
        "volume": lots,
        "type": mt5.ORDER_TYPE_BUY,
        "action": mt5.TRADE_ACTION_DEAL, #at market
        "type_time": mt5.ORDER_TIME_DAY,
        "type_filling": mt5.ORDER_FILLING_RETURN
    }

    try:
        print(f"\n>>> BUY order sent: {request}")
        result = mt5.order_send(request) 
        print(f"    RESULT: {result}")
        return result.order
    except:
        print(f"    FAILED: {mt5.last_error()}")
    return ""

def sell_limit(mt5, stock, lots, price):
    request = { 
        "symbol": stock, 
        "volume": lots,
        "price": price,
        "type": mt5.ORDER_TYPE_SELL_LIMIT,
        "action": mt5.TRADE_ACTION_PENDING,
        "type_time": mt5.ORDER_TIME_DAY,
        "type_filling": mt5.ORDER_FILLING_RETURN
    }

    try:
        print(f"\n>>> SELL order sent: {request}")
        result = mt5.order_send(request) 
        print(f"    RESULT: {result}")
        return result.order
    except:
        print(f"    FAILED: {mt5.last_error()}")
    return ""