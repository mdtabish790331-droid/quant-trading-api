from data_loader import load_data
from strategy.moving_average import generate_signals
from backtest.engine import backtest
from backtest.metrics import calculate_profit, calculate_return

stock = "INFY"

df = load_data(stock)

df = generate_signals(df)

final_value, trades = backtest(df)

profit = calculate_profit(100000, final_value)
returns = calculate_return(100000, final_value)

print("Stock:", stock)
print("Final Value:", final_value)
print("Profit:", profit)
print("Return %:", returns)
print("Trades:", trades)