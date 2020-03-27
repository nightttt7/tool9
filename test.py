# TODO: change this file for unittest

# %%
import pandas as pd
from pathlib import Path
from tool9 import RRP, period, es, performance, portfolio_risk, period_4_plot

test_data_path = Path('test_data/')

# %%
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

# %%
# test RRP
logr = pd.read_csv(test_data_path / 'testdata-logr.csv',
                   parse_dates=['Date'], index_col='Date')
risk = pd.read_csv(test_data_path / 'testdata-risk.csv',
                   parse_dates=['Date'], index_col='Date')
corr = pd.read_csv(test_data_path / 'testdata-corr.csv',
                   parse_dates=['Date'], index_col=[0, 1])
first_reset_date = '2007-08-07'
reset_months = 6
target_risk = 10.324


portfolio1 = RRP(ratio_fixed=None, logr=logr, risk=risk, corr=corr,
                 first_reset_date=first_reset_date, reset_months=reset_months,
                 reset_shift_mode='after', target_risk=target_risk,
                 leverage_fixed=None, leverage_limit=None, get_actual=True)
