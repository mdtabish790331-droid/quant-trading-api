from utils.indicators import moving_average

def generate_signals(df):
    df['ma20'] = moving_average(df['close'], 20)
    df['ma50'] = moving_average(df['close'], 50)

    df['signal'] = 0

    for i in range(1, len(df)):
        if df['ma20'][i] > df['ma50'][i] and df['ma20'][i-1] <= df['ma50'][i-1]:
            df['signal'][i] = 1   # BUY

        elif df['ma20'][i] < df['ma50'][i] and df['ma20'][i-1] >= df['ma50'][i-1]:
            df['signal'][i] = -1  # SELL

    return df