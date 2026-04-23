import pandas as pd

def moving_average(series, window):
    return series.rolling(window=window).mean()

def generate_signals(df):
    df = df.copy()
    df['close'] = pd.to_numeric(df['close'], errors='coerce')
    df['ma20'] = df['close'].rolling(window=20).mean()
    df['ma50'] = df['close'].rolling(window=50).mean()
    df['signal'] = 0

    for i in range(1, len(df)):
        try:
            if (df['ma20'].iloc[i] > df['ma50'].iloc[i] and
                df['ma20'].iloc[i-1] <= df['ma50'].iloc[i-1]):
                df.iloc[i, df.columns.get_loc('signal')] = 1
            elif (df['ma20'].iloc[i] < df['ma50'].iloc[i] and
                  df['ma20'].iloc[i-1] >= df['ma50'].iloc[i-1]):
                df.iloc[i, df.columns.get_loc('signal')] = -1
        except:
            pass
    return df