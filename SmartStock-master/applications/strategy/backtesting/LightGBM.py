# -*- coding: UTF-8 -*-
"""
@Author  ：leven

@Date    ：2025/2/25 13:20

@mark    :
"""
import pandas as pd
import numpy as np
import akshare as ak
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# 参数设置
LOOKBACK_WINDOW = 30  # 回看窗口
FORECAST_HORIZON = 5  # 预测未来5分钟
THRESHOLD = 0.6  # 交易信号阈值


# 获取股票数据（示例使用akshare获取分钟级数据）
def get_stock_data(symbol, period="5"):
    df = ak.stock_zh_a_hist_min_em(symbol=symbol, period=period, adjust='')
    df['timestamp'] = pd.to_datetime(df['时间'])
    df = df.set_index('timestamp').sort_index()
    return df[['开盘', '最高', '最低', '收盘', '成交量']]


# 特征工程
def create_features(df):
    # 基础特征
    df['returns'] = df['收盘'].pct_change()

    # 技术指标
    df['ma5'] = df['收盘'].rolling(5).mean()
    df['ma20'] = df['收盘'].rolling(20).mean()
    df['volatility'] = df['returns'].rolling(20).std()

    # 量价特征
    df['volume_change'] = df['成交量'].pct_change()
    df['price_volume_corr'] = df['收盘'].rolling(20).corr(df['成交量'])

    # 滞后特征
    for lag in [1, 2, 3, 5]:
        df[f'return_lag_{lag}'] = df['returns'].shift(lag)

    # 目标变量：未来N分钟是否上涨
    df['target'] = (df['收盘'].shift(-FORECAST_HORIZON) > df['收盘']).astype(int)

    return df.dropna()


# 训练LightGBM模型
def train_model(X_train, y_train):
    params = {
        'objective': 'binary',
        'metric': 'binary_logloss',
        'learning_rate': 0.05,
        'num_leaves': 31,
        'feature_fraction': 0.8,
        'bagging_fraction': 0.8,
        'verbosity': -1
    }

    train_data = lgb.Dataset(X_train, label=y_train)
    model = lgb.train(params, train_data, num_boost_round=1000)
    return model


# 生成交易信号
def generate_signals(model, X):
    preds = model.predict(X)
    signals = pd.Series(0, index=X.index)
    signals[preds > THRESHOLD] = 1  # 做多
    signals[preds < (1 - THRESHOLD)] = -1  # 做空
    return signals


# 回测策略
def backtest(signals, prices):
    returns = prices.pct_change().shift(-1)
    strategy_returns = signals.shift(1) * returns
    return strategy_returns.cumsum()


# 主流程
if __name__ == "__main__":
    # 获取数据（示例股票：平安银行）
    data = get_stock_data("000001", period="5")

    # 特征工程
    df = create_features(data)

    # 数据预处理
    features = df.drop(columns=['target', '收盘'])
    target = df['target']
    X_train, X_test, y_train, y_test = train_test_split(
        features, target, test_size=0.2, shuffle=False)

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # 训练模型
    model = train_model(X_train, y_train)

    # 生成信号
    # 将 X_test 转换回 DataFrame 类型，使用原始数据的索引
    X_test_df = pd.DataFrame(X_test, index=features.iloc[-len(X_test):].index, columns=features.columns)
    signals = generate_signals(model, X_test_df)

    # 回测
    test_prices = df.iloc[-len(X_test):]['收盘']
    cumulative_returns = backtest(signals, test_prices)

    # 评估
    print(f"模型准确率: {accuracy_score(y_test, model.predict(X_test).round())}")
    cumulative_returns.plot(title="Strategy Cumulative Returns")
    plt.show()