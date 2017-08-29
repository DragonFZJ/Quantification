# -*- coding: utf-8 -*-
"""
@量化交流QQ群: 461470781
"""
import pandas as pd


# =====导入月线数据
# 注意：filepath_or_buffer参数中请填写数据在你电脑中的路径
stock_data = pd.read_csv(filepath_or_buffer='stock_data.csv', parse_dates=[u'交易日期'], encoding='gbk')

# =====计算每个股票下个月的涨幅
stock_data[u'下个月涨跌幅'] = stock_data.groupby(u'股票代码')[u'涨跌幅'].shift(-1)

# =====删除一些不满足条件的股票数据
# 删除在某些月份市净率小于0的股票
stock_data = stock_data[stock_data[u'市净率'] > 0]
# 删除在当月最后一个交易日停牌的股票
stock_data = stock_data[stock_data[u'是否交易'] == 1]
# 删除在当月最后一个交易日涨停的股票
stock_data = stock_data[stock_data[u'是否涨停'] == 0]
# 删除在本月交易日小于10天的股票
stock_data = stock_data[stock_data[u'交易天数'] > 10]
# 删除2000年之前的股票数据
stock_data = stock_data[stock_data[u'交易日期'] > pd.to_datetime('20000101')]
# 删除"下个月涨跌幅"字段为空的行
stock_data.dropna(subset=[u'下个月涨跌幅'], inplace=True)

# =====选股
stock_data[u'factor'] = stock_data[u'总市值'] * stock_data[u'市净率']
stock_data = stock_data.sort([u'交易日期', u'factor'])  # 排序
stock_data = stock_data.groupby([u'交易日期']).head(10)  # 选取前十名的股票

# =====计算每月选股收益
output = pd.DataFrame()
stock_data[u'股票代码'] += u' '
stock_data_groupby = stock_data.groupby(u'交易日期')
output[u'买入股票'] = stock_data_groupby[u'股票代码'].sum()
output[u'股票数量'] = stock_data_groupby.size()
output[u'买入股票下月平均涨幅(%)'] = stock_data_groupby[u'下个月涨跌幅'].mean()
output[u'下个月末的资金(初始100)'] = (output[u'买入股票下月平均涨幅(%)']+1.0).cumprod() * 100.0
output.reset_index(inplace=True)

# ======输出
output.to_csv('output.csv', index=False, encoding='gbk')
