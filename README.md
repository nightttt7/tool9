# tool9
A tool for portfolio management, based on the codes for my master thesis 

# class RRP
construct a risk parity portfolio

construct a risk parity portfolio ('RPP') or fixed ratio portfolio ('FRP')
(when ratio_fixed provided).

must input logr, reset_months  
if use FRP, input ratio_fixed  
if use RRP, input risk, corr(more than 2 assets, UnfinishedFeature)  
if use fixed leverate, input leverage_fixed  
if have target risk, input target_risk, risk and corr  
first_reset_date and leverage_limit is optional

use new_[input] to renew input and construct new portfolio

Attributes:

[input]
```
ratio_fixed: list, a fixed ratio of assets, !!construct FRP if provided

logr: log return of assets, pd.DataFrame with column be asset name, index be datetime

risk: risk of assets, pd.DataFrame with column name be risk name, index be datetime

corr: correlation between assets for each observation, pd.DataFrame with column name be asset name, outer index be datetime, inner index be asset name

first_reset_date: string or datetime, reset at the begining of day

reset_months: int, number of months between two reset date

reset_shift_mode: determine whether take the first trading day after or before the planed reset date as real reset date

target_risk: int, if target_risk is provided, the leverage of portfolio will be set so that portfolio risk will equal to the target_risk 

leverage_fixed: number, !!if provided, the leverage of portfolio will not change and always be it

leverage_limit: number, if provided, leverage won't be higher than it

get_actual: default False, get actual ratio, portfolio risk and actual portfolio risk
```

[output]
```
sample_month_interval: total months in sample period

reset_times: times of reset

reset_date: pd.DatetimeIndex, the date of reset dates

logr_p: portfolio log return, pd.DataFrame with column name be asset name, index be datetime

ratio: retio of assets, pd.DataFrame with column name be asset name, index be datetime

ratio_actual: actual ratio of assets, pd.DataFrame with column name be asset name, index be datetime

risk_p: portfolio risk, pd.DataFrame with column name be 'portfolio',
index be datetime
        
risk_p_actual: actual portfolio risk, pd.DataFrame with column name be
'portfolio', index be datetime
    
leverage: leverage of portfolio, pd.DataFrame with column name be 'leverage', index be datetime
```

# function period
return the effective date period of one column
```
period(col, data)
```
return: `[start, end]`

# function describe
```
describe(col, data)
```

# function ni 
(no included)
```
ni(col, data)
```

# lr
log returns of protfolio, main input. because of the characteristic of logarithm, all the performances reflect the relatively performances in log returns, but not absolute performances.

# function profit
(sum log return)
```
profit(lr)
```

# function sr
(yearly sharpe ratio (no risk free rate) for returns)  
(not log returns here)
```
sr(lr)
```

# function var
(value at risk for log returns)
```
var(lr, *level)
```

# function es
(expected shortfall for log returns)
```
es(lr, *level)
```

# function drawdown 
(cumulative log returns drawdown)  
attention: only this function returns a series
```
drawdown(lr)
```


# function maxdrawdown
(maximum cumulative log returns drawdown)
```
maxdrawdown(lr)
```

# function performance
(all the performances for log returns)
```
performance(lr, level)
```

# function portfolio_risk
```
portfolio_risk(data_corr, data_vol, data_ratio)
```

# function period_4_plot
```
period_4_plot(start, end, n)
```
