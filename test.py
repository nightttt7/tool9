# used in VScode
# TODO: change this file for unittest
import pandas as pd
from pathlib import Path
from tool9 import RRP, period, es, performance, portfolio_risk, period_4_plot

test_data_path = Path('test_data/')

# test RRP.month_interval
tmp_date1 = pd.to_datetime('2011-01-05')
tmp_date2 = pd.to_datetime('2012-01-04')
tmp_date3 = pd.to_datetime('2012-01-05')
tmp_date4 = pd.to_datetime('2012-01-06')
print("no information means good")
if not RRP.month_interval(tmp_date1, tmp_date2) == 11:
    print('function month_interval wrong')
if not RRP.month_interval(tmp_date1, tmp_date3) == 12:
    print('function month_interval wrong')
if not RRP.month_interval(tmp_date1, tmp_date4) == 12:
    print('function month_interval wrong')

# test RRP
RRP_test_data = pd.read_csv(test_data_path / 'testdata1.csv',
                            parse_dates=['Date'],
                            index_col='Date')
logr = RRP_test_data[['return1', 'return2']]
risk = RRP_test_data[['volatility1', 'volatility2']]
corr = RRP_test_data[['return1', 'return2']].corr()
first_reset_date = '2003-01-08'
reset_months = 12
target_risk = 10


portfolio1 = RRP(ratio_fixed=None, logr=logr, risk=risk, corr=corr,
                 first_reset_date=first_reset_date, reset_months=reset_months,
                 reset_shift_mode='after', target_risk=target_risk,
                 leverage_fixed=None, leverage_limit=None, get_actual=True)
