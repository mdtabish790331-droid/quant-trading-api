def moving_average(series, window):
    return series.rolling(window=window).mean()

def generate_signals(df):
    df['ma20'] = moving_average(df['close'], 20)
    df['ma50'] = moving_average(df['close'], 50)
    df['signal'] = 0

    for i in range(1, len(df)):
        if df['ma20'].iloc[i] > df['ma50'].iloc[i] and df['ma20'].iloc[i-1] <= df['ma50'].iloc[i-1]:
            df['signal'].iloc[i] = 1   # BUY
        elif df['ma20'].iloc[i] < df['ma50'].iloc[i] and df['ma20'].iloc[i-1] >= df['ma50'].iloc[i-1]:
            df['signal'].iloc[i] = -1  # SELL

    return df