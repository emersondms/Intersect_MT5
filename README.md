# Intersect_MT5
Trading bot for the MetaTrader 5 platform

# Concept
- A **Swing Trade** strategy **(for IBOVESPA market)** that buys stocks that the **closing price is near the low price (small tail)**, and sells it **tomorrow in today's HALF price**, like in the image below:

![Example](https://user-images.githubusercontent.com/7670466/164803205-d46f4ad5-2a21-4632-86b8-2690ff80e027.png)

- The script will sort the stocks from **intersect_backtest.csv (2021)** by the **highest profit factor**;
- Only daily candles (D1) are considered;
- After each 'runner' script execution, an e-mail will be sent with the logging details.

# Setup
    - Python 3.8;
    - MetaTrader 5 configured with a trading account and Algotrading enabled;
    - E-mail details filled on strategy.properties file;
    - Any task scheduler;
    - pip install MetaTrader5
    - pip install pandas
    - pip install jproperties


# Execution
## runner_buy_stocks.py

- To be scheduled at: on the last minutes of negotiation time **(16:50)**;  
- Number of stocks to be bought **at market**: **strategy.properties\NUMBER_OF_POSITIONS_TO_OPEN** 
- If an already bought stock is matching the strategy again, it will have priority (to decrease the average price);
- Amount of money to be invested for each stock: **strategy.properties\MONEY_STAKE_FOR_EACH_POSITION**
- **The property above** and the **stock closing price** will be used to calculate the **size of the lots** to be applied.

## runner_take_profit.py

- To be scheduled at: the market opening time **(10:00)**; 
- For all opened positions, this script will open **sell limit orders** on **yesterday's half price**.

## runner_close_positions.py

- To be scheduled at: near the market closing time **(16:45)**;
- For positions that still did not reach the **take profit orders**, this script will close the ones **opened 2 days ago**, or that the **closing price is higher than half price**. 