from utils.strategy.backtest.metrics import calculate_profit, calculate_return

def backtest(df, initial_capital=100000):
    capital = initial_capital
    position = 0
    entry_price = 0
    trades = []

    for i in range(len(df)):
        signal = df['signal'].iloc[i]
        price = df['close'].iloc[i]

        if signal == 1 and position == 0:
            position = capital / price
            entry_price = price
            capital = 0
            trades.append(f"BUY at {round(price, 2)}")

        elif signal == -1 and position > 0:
            capital = position * price
            profit = (price - entry_price) * position
            position = 0
            trades.append(f"SELL at {round(price, 2)} | Profit: {round(profit, 2)}")

    final_value = capital + (position * df['close'].iloc[-1])
    
    print(f"✅ Final Value: {round(final_value, 2)}")
    print(f"✅ Total Return: {round(calculate_return(initial_capital, final_value), 2)}%")

    return final_value, trades