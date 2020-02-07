# used in VScode
# TODO: change this file for unittest
# %%
import pandas as pd
from pathlib import Path
from class_rrp import RRP

# %%
tmp_date1 = pd.to_datetime('2011-01-05')
tmp_date2 = pd.to_datetime('2012-01-04')
tmp_date3 = pd.to_datetime('2012-01-05')
tmp_date4 = pd.to_datetime('2012-01-06')
if not RRP.month_interval(tmp_date1, tmp_date2) == 11:
    print('function month_interval wrong')
if not RRP.month_interval(tmp_date1, tmp_date3) == 12:
    print('function month_interval wrong')
if not RRP.month_interval(tmp_date1, tmp_date4) == 12:
    print('function month_interval wrong')

# %%
test_data_path = Path('test_data/')
logr = pd.read_pickle(test_data_path / 'temp1')
risk = pd.read_pickle(test_data_path / 'temp2')
corr = pd.read_pickle(test_data_path / 'temp3')
first_reset_date = '2002-09-05'
reset_months = 12
target_risk = 10.322026977821176

# %%
portfolio1 = RRP(ratio_fixed=None, logr=logr, risk=risk, corr=corr,
                 first_reset_date=first_reset_date, reset_months=reset_months,
                 reset_shift_mode='after', target_risk=target_risk,
                 leverage_fixed=None, leverage_limit=None, get_actual=True)


# %%
