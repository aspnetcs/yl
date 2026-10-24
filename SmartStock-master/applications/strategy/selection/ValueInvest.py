# -*- coding: UTF-8 -*-
"""
@Author  ：leven

@Date    ：2025/2/25 17:17

@mark    : 价值投资
"""
import akshare as ak
import pandas as pd
from gm.api import *
from datetime import datetime

def get_financial_data(stock_code):
    """
    获取单只股票的财务数据
    参数：
        stock_code : 股票代码（如 '600519'）
    返回：
        DataFrame : 包含财务指标的DataFrame
    """
    try:
        # 获取财务数据
        df = ak.stock_financial_abstract_ths(symbol=stock_code, indicator="按报告期")  # 替换为 stock_financial_abstract_ths
        # 去掉百分号并转换为小数
        df['净资产收益率'] = df['净资产收益率'].str.rstrip('%').astype(float) / 100
        df['销售毛利率'] = df['销售毛利率'].str.rstrip('%').astype(float) / 100
        df['资产负债率'] = df['资产负债率'].str.rstrip('%').astype(float) / 100
        df['流动比率'] = df['流动比率'].str.rstrip('%').astype(float) / 100
        df['每股经营现金流'] = df['每股经营现金流'].str.rstrip('%').astype(float) / 100
        # 提取关键指标
        financial_data = {
            'roe': df['净资产收益率'].values[0],
            'gross_margin': df['销售毛利率'].values[0],
            'debt_ratio': df['资产负债率'].values[0],
            'current_ratio': df['流动比率'].values[0],
            'operating_cash_flow': df['每股经营现金流'].values[0],
        }
        return pd.DataFrame([financial_data])
    except Exception as e:
        print(f"获取 {stock_code} 财务数据失败: {e}")
        return pd.DataFrame()

tt = get_financial_data('600519')

def get_valuation_data(stock_code):
    """
    获取单只股票的估值数据
    参数：
        stock_code : 股票代码（如 '600519'）
    返回：
        DataFrame : 包含估值指标的DataFrame
    """
    try:
        stock_value_em_df = ak.stock_value_em(symbol=stock_code)
        stock_a_indicator_lg_df = ak.stock_a_indicator_lg(symbol=stock_code)
        # 获取估值数据
        df = ak.stock_zh_a_spot_em()
        #从df中提取代码是stock_code的行
        df = df[df['代码'] == stock_code]
        valuation_data = {
            'pe': df['市盈率-动态'].values[0],
            'pb': df['市净率'].values[0],
            'peg': stock_value_em_df['PEG值'].values[0],
            'dividend_yield': stock_a_indicator_lg_df['dv_ttm'].values[0],
        }
        return pd.DataFrame([valuation_data])
    except Exception as e:
        print(f"获取 {stock_code} 估值数据失败: {e}")
        return pd.DataFrame()


def get_industry_data(stock_code):
    """
    获取指定股票所在行业的增长率和行业市盈率
    :param stock_code: 股票代码，如 '600519'
    :return: 行业增长率和行业市盈率
    """
    # 获取股票所属行业信息
    stock_info = ak.stock_individual_info_em(symbol=stock_code)
    industry_name = stock_info.loc[stock_info['item'] == '行业', 'value'].values[0]  # 获取所属行业名称[^13^]
    # 获取该行业成分股信息
    industry_cons_df = ak.stock_board_industry_cons_em(symbol=industry_name)
    industry_cons_df = industry_cons_df[industry_cons_df['代码'] != stock_code]  # 排除自身股票[^9^]
    industry_cons_df = list(industry_cons_df['代码'].apply(em_code).values)
    df = stk_get_finance_deriv_pt(symbols=industry_cons_df, fields='oper_prof_yoy', df=True)
    dv = stk_get_daily_valuation_pt(symbols=industry_cons_df, fields='pe_ttm', df=True)

    df.index = df.symbol
    dv.index = dv.symbol

    df['pe_ttm'] = dv['pe_ttm']
    try:
        # 获取行业数据
        industry_data = {
            'industry_growth': df['oper_prof_yoy'].mean(),
            'industry_pe': df['pe_ttm'].mean(),
        }
        return pd.DataFrame([industry_data])
    except Exception as e:
        print(f"获取 {stock_code} 行业数据失败: {e}")
        return pd.DataFrame()

def evaluate_financial_health(df, weights=None):
    """
    评估财务健康度（每项达标得1分，满分5分）
    参数：
        df : DataFrame，需包含以下字段：
            'roe', 'gross_margin', 'debt_ratio',
            'current_ratio', 'operating_cash_flow'
        weights : 各项权重（默认等权重）
    返回：
        DataFrame : 增加财务分的DataFrame
    """
    if weights is None:
        weights = [0.2, 0.2, 0.2, 0.2, 0.2]  # 默认等权重

    df['财务分'] = 0

    # ROE > 15%
    df['财务分'] += df['roe'].apply(lambda x: weights[0] if x > 0.15 else 0)

    # 毛利率 > 40%
    df['财务分'] += df['gross_margin'].apply(lambda x: weights[1] if x > 0.4 else 0)

    # 资产负债率 < 50%
    df['财务分'] += df['debt_ratio'].apply(lambda x: weights[2] if x < 0.5 else 0)

    # 流动比率 > 1.5
    df['财务分'] += df['current_ratio'].apply(lambda x: weights[3] if x > 1.5 else 0)

    # 经营现金流为正
    df['财务分'] += df['operating_cash_flow'].apply(lambda x: weights[4] if x > 0 else 0)

    return df


def evaluate_valuation(df, industry_pe, weights=None):
    """
    评估估值合理性（每项达标得1分，满分4分）
    参数：
        df : 包含PE/PB/PEG/dividend_yield的DataFrame
        industry_pe : 行业平均PE
        weights : 各项权重（默认等权重）
    返回：
        DataFrame : 增加估值分的DataFrame
    """
    if weights is None:
        weights = [0.25, 0.25, 0.25, 0.25]  # 默认等权重

    df['估值分'] = 0

    # PE低于行业平均
    df['估值分'] += df['pe'].apply(lambda x: weights[0] if x < industry_pe else 0)

    # PB < 1.5
    df['估值分'] += df['pb'].apply(lambda x: weights[1] if x < 1.5 else 0)

    # PEG < 1（需处理除零错误）
    df['估值分'] += df.apply(
        lambda row: weights[2] if (row['peg'] < 1) and (row['peg'] > 0) else 0,
        axis=1
    )

    # 股息率 > 3%
    df['估值分'] += df['dividend_yield'].apply(lambda x: weights[3] if x > 0.03 else 0)

    return df


def value_investing_screen(stock_codes, financial_weights=None, valuation_weights=None):
    """
    综合价值投资筛选
    参数：
        stock_codes : 股票代码列表（如 ['600519', '000858']）
        financial_weights : 财务健康度权重
        valuation_weights : 估值合理性权重
    返回：
        DataFrame : 筛选结果
    """
    results = []
    print(f"股票数量为{len(stock_codes)}")
    for code in stock_codes:
        # 获取数据
        financial_df = get_financial_data(code)
        valuation_df = get_valuation_data(code)
        industry_df = get_industry_data(code)

        if financial_df.empty or valuation_df.empty or industry_df.empty:
            continue

        # 合并数据
        df = pd.concat([financial_df, valuation_df, industry_df], axis=1)

        # 评估财务健康度
        df = evaluate_financial_health(df, weights=financial_weights)

        # 评估估值合理性
        df = evaluate_valuation(df, industry_pe=df['industry_pe'].values[0], weights=valuation_weights)

        # 计算总分
        df['总分'] = df['财务分'] + df['估值分']
        df['代码'] = code
        results.append(df)

    if not results:
        return pd.DataFrame()

    # 合并所有结果并筛选
    result_df = pd.concat(results)
    result_df = result_df[result_df['pe'] > 0]
    result_df = result_df[result_df['pe'] < 50]
    result_df = result_df[result_df['pb'] > 0]
    result_df = result_df[result_df['pb'] < 5]
    result_df = result_df[result_df['gross_margin'] > 0.4]
    result_df = result_df[result_df['roe'] > 0.15]
    # 按总分排序并取前20
    return result_df[result_df['总分'] > 0.7].sort_values('总分', ascending=False).head(50)

def em_code(symbol):
    """
    用于处理其他系统的股票代码和掘金量化的股票代码的一致性
    :param symbol: 股票代码字符串
    :return: 格式化后的股票代码字符串
    """
    # 输入验证
    if not isinstance(symbol, str) or len(symbol) < 1:
        raise ValueError("输入必须是非空字符串。")

    # 使用字典映射来简化逻辑，提高可读性和可维护性
    exchange_mapping = {
        '6': 'SHSE',
        '0': 'SZSE',
        '2': 'SZSE',
        '3': 'SZSE'
    }

    # 检查并处理股票代码
    for digit, exchange in exchange_mapping.items():
        if symbol[0] == digit:
            return f"{exchange}.{symbol}"

    # 如果没有匹配到任何交易所，返回原始股票代码
    return symbol

# 示例使用
if __name__ == "__main__":
    set_token('xxxx')
    end_date = datetime.now()
    # 获取上一个交易日的日期
    last_day = get_previous_trading_date(exchange='SHSE', date=end_date)
    # 获取沪深300成份股
    stock_codes = stk_get_index_constituents(index='SHSE.000300')['symbol']
    # 获取数字部分
    stock_codes = [item[5:] for item in stock_codes if True]
    # 过滤掉以 "3", "8", "9", "2", "4" 开头的代码
    stock_codes = [code for code in stock_codes if not code.startswith(('3', '8', '9', '2', '4', '68'))]
    # 股票代码列表
    # stock_codes = ['600519', '000858', '600036']
    # 执行筛选
    result = value_investing_screen(stock_codes)

    # 输出结果
    if not result.empty:
        print(result['代码'].values)
        print(result[['代码','roe', 'gross_margin', 'pe', 'pb', '总分']])
    else:
        print("未找到符合条件的股票。")