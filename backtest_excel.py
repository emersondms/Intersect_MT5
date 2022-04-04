import xlrd

def get_stocks_dict(excel_path):
    """Returns the backtest excel content
    @param excel_path: backtest sheet path
    @returns stocks_dict: a dictionary with <stock_name, profit_factor> 
    """

    worbook = xlrd.open_workbook(excel_path)
    sheet = worbook.sheet_by_index(0)
    stocks_dict = {}
    
    for row in range(sheet.nrows): 
        row_value = sheet.row_values(row)
        if row_value[0] == "STOCK_NAME": continue
        stocks_dict[row_value[0]] = row_value[1]
    
    return stocks_dict
