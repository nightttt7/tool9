# manual test

# %%
import pandas as pd
import numpy as np
from pandas.api.types import is_datetime64_any_dtype
from pathlib import Path
from tool9 import RRP, period, es, performance, portfolio_risk, period_4_plot

test_data_path = Path('test_data/')

# %%
# test RRP
logr = pd.read_csv(test_data_path / 'testdata-logr.csv',
                   parse_dates=['Date'], index_col='Date')
risk = pd.read_csv(test_data_path / 'testdata-risk.csv',
                   parse_dates=['Date'], index_col='Date')
corr = pd.read_csv(test_data_path / 'testdata-corr.csv',
                   parse_dates=['Date'], index_col=[0, 1])
rf = pd.read_csv(test_data_path / 'testdata-rf.csv',
                 parse_dates=['Date'], index_col='Date')
rf_rolling = rf.rolling(250).mean()['2007-08-01':'2016-01-04']
r_rolling = pd.read_csv(test_data_path / 'testdata-rrolling.csv',
                        parse_dates=['Date'], index_col='Date')

first_reset_date = '2007-08-07'
reset_months = 6
target_risk = 10.324

# %%
p = RRP(ratio_fixed=[0.6, 0.4], logr=logr, risk=None, corr=corr,
        first_reset_date=None, reset_months=reset_months,
        reset_shift_mode='after', target_risk=None,
        leverage_fixed=None, leverage_limit=None, get_actual=False)

# %%
p = RRP(ratio_fixed=None, logr=logr, risk=risk, corr=corr,
        first_reset_date=first_reset_date, reset_months=reset_months,
        reset_shift_mode='after', target_risk=target_risk,
        leverage_fixed=None, leverage_limit=None, get_actual=True)

# %%
# test usekelly
p = RRP(ratio_fixed=None, logr=logr, risk=risk, corr=corr,
        first_reset_date=first_reset_date, reset_months=reset_months,
        reset_shift_mode='after', target_risk=None,
        usekelly=True, rf_rolling=rf_rolling, r_rolling=r_rolling,
        leverage_fixed=None, leverage_limit=None, get_actual=True)

p.leverage.plot()

# %%
