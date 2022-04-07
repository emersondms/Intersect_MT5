def get_position_lots(mt5_conn, stock):
    '''Returns the position lots size for the stock
    @param mt5_conn: MetaTrader5 connection object
    @param stock: name
    @returns: position size as float
    '''

    positions_opened = mt5_conn.positions_get(symbol=stock)
    position_size = 0

    if not positions_opened == None:
        if len(positions_opened) > 0:
            position_size = float(positions_opened[0].volume)

    return position_size

def calculate_lots_size(money_stake, stock_price):
    '''Returns the lots size for the given parameters
    @param money_stake: MetaTrader5 connection object
    @param stock_price: as float
    @returns: lots size as float
    '''

    total = money_stake / stock_price

    # round down to nearest 100 multiple
    lots_size = float(int(total - (total % 100)))
    return lots_size

def get_total_of_positions_opened(mt5_conn):
    return int(mt5_conn.positions_total())