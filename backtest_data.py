#import xlrd
import csv

def get_stocks_dict():
    """Returns the backtest csv content
    @returns stocks_dict: a dictionary with <stock_name, profit_factor> 
    """
    csv_path = r"intersect_backtest.csv"
    with open(csv_path, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        stocks_dict = {}
        for row in csv_reader:
            stocks_dict[row["STOCK_NAME"]] = row["PROFIT_FACTOR"]   

        return stocks_dict
        
'''
def get_stocks_dict():
    """Returns the backtest excel content
    @returns stocks_dict: a dictionary with <stock_name, profit_factor> 
    """
    excel_path = r"intersect_backtest.xlsx"
    worbook = xlrd.open_workbook(excel_path)
    sheet = worbook.sheet_by_index(0)
    stocks_dict = {}
    
    for row in range(sheet.nrows): 
        row_value = sheet.row_values(row)
        if row_value[0] == "STOCK_NAME": continue
        stocks_dict[row_value[0]] = row_value[1]
    
    return stocks_dict
'''