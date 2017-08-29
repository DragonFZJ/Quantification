# -*- coding: utf-8 -*-
"""
量化交流Q群：461470781，欢迎加入。
"""
import os
import pandas as pd

# ========== 遍历数据文件夹中所有股票文件的文件名，得到股票文件名列表file_list
file_list = []
for root, dirs, files in os.walk('zhubi-2015-05-19/data'):  # 注意：这里请填写数据文件在您电脑中的路径
    if files:
        for f in files:
            if '.csv' in f:
                file_list.append(f.split('.csv')[0])


# ========== 根据上一步得到的文件名列表，遍历所有股票，计算每个股票的资金流数据，放入output变量
output = pd.DataFrame()

# ===遍历每个股票
for f in file_list:
    code = f.split()[-1].strip()  # 读取股票代码
    print code

    # 读取数据
    stock_data = pd.read_csv('zhubi-2015-05-19/data/' + f + '.csv',
                             parse_dates=[0])  # 注意：这里请填写数据文件在您电脑中的路径，注意斜杠方向

    stock_data['Money'] = stock_data['Volume'] * stock_data['Price']  # 计算每笔交易成交额

    l = len(output)
    output.loc[l, 'code'] = code
    output.loc[l, '平均每笔交易成交量'] = stock_data['Volume'].mean()

    # 计算资金流入流出
    data = stock_data.groupby('BuySell')['Money'].sum()
    if 'B' in data.index:
        output.loc[l, '资金流入'] = data['B']
    if 'S' in data.index:
        output.loc[l, '资金流出'] = data['S']

    # 计算主力资金流入流出
    data = stock_data[stock_data['Volume'] > 50000].groupby('BuySell')['Money'].sum()
    if 'B' in data.index:
        output.loc[l, '主力资金流入'] = data['B']
    if 'S' in data.index:
        output.loc[l, '主力资金流出'] = data['S']

# ========== 输出每个股票的资金流数据到csv文件，用中文excel或者wps打开查看
output.to_csv('资金流数据.csv', index=False, encoding='gbk')

