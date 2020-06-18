__all__ = ['period', 'describe', 'ni', 'profit', 'sr', 'srf', 'var', 'es',
           'drawdown', 'avedrawdown', 'maxdrawdown', 'performance',
           'portfolio_risk', 'period_4_plot', 'performance1']


# ----------------------------------------------------------------------------


def period(col, data):
    """
    return the effective date period of one column
    """
    start = data[col].first_valid_index()
    end = data[col].sort_index(ascending=False).first_valid_index()
    return([start, end])
# how to use:
# [start,end] = period('colname')
# ----------------------------------------------------------------------------


def describe(col, data):
    """
    return basic statistical descriptions
    """
    import pandas as pd
    d = {}
    # number of observations
    d['Nobs'] = [data[col].count()]
    # mean
    d['Mean'] = [data[col].mean()]
    # std
    d['Std.'] = [data[col].std()]
    # mad
    d['Mad'] = [data[col].mad()]
    # min
    d['Min'] = [data[col].min()]
    # max
    d['Max'] = [data[col].max()]
    # skew
    d['Skew'] = [data[col].skew()]
    # excess kurt
    d['Excess Kurt'] = data[col].kurt()
    # acf lag=1
    d['acf lag=1'] = data[col].autocorr(1)
    # acf lag=5
    d['acf lag=5'] = data[col].autocorr(5)
    # acf lag=10
    d['acf lag=10'] = data[col].autocorr(10)
    # acf lag=20
    d['acf lag=20'] = data[col].autocorr(20)
    # turn to DataFrame
    output = pd.DataFrame(d)
    # rename index
    output.index = [col]
    return(output)
# ----------------------------------------------------------------------------


# function ni (no included)
def ni(col, data):
    return(data.loc[:, data.columns != col])
# how to use:
# col_ni = ni('colname')
# ----------------------------------------------------------------------------


# those functions is about the performance of log returns

# lr: log returns, main input.
# lrf: log risk free rate
# because of the characteristic of logarithm, profit, var and es
#   reflect the relatively performances in log returns

# function profit (sum log return)
def profit(lr):
    t = lr.sum()
    return t


# function sr (yearly sharpe ratio (no risk free rate) for log returns)
def sr(lr):
    import numpy as np
    s = lr.std()
    t = (lr.mean()/s)*np.sqrt(252)
    return t


# function srf (yearly sharpe ratio for (excess) log returns)
# use log risk-free rate to get the excess return
def srf(lr, lrf):
    import numpy as np
    s = (lr-lrf).std()
    t = ((lr.mean()-lrf.mean())/s)*np.sqrt(252)
    return t


# function var (value at risk for log returns)
# with confindence level 0.95
def var(lr):
    import numpy as np
    n = int(np.ceil(lr.count()*0.95))
    t = lr.sort_values(ascending=False)[n-1]
    return t


# function es (expected shortfall for log returns)
# with confindence level 0.95
def es(lr):
    import numpy as np
    n = int(np.ceil(lr.count()*0.95))
    t = lr.sort_values(ascending=False)[n-1:].mean()
    return t


# function drawdown (percentage drawdown)
# (not log returns here)
# attention: only this function returns a series
def drawdown(lr):
    import numpy as np
    clr = lr.cumsum()
    cummax = clr.cummax()
    t = clr-cummax
    t = np.exp(t)-1
    return t


# function average drawdown
def avedrawdown(lr):
    t = drawdown(lr).mean()
    return t


# function maxdrawdown (max percentage drawdown)
# (not log returns here)
def maxdrawdown(lr):
    import numpy as np
    clr = lr.cumsum()
    cummax = clr.cummax()
    t = (clr-cummax).min()
    t = np.exp(t)-1
    return t


# function performance (all the performances for log returns)
def performance(lr):
    import pandas as pd
    t = pd.DataFrame([profit(lr), sr(lr), var(lr), es(lr),
                      maxdrawdown(lr)])
    t.index = ['profit', 'sharpe ratio', 'VaR', 'ES', 'maxdrawdown']
    t.columns = ['performance']
    return t.T


# function performance (all the performances for log returns)
def performance1(lr, lrf):
    import pandas as pd
    t = pd.DataFrame([profit(lr), avedrawdown(lr), srf(lr, lrf), var(lr),
                      es(lr), maxdrawdown(lr)])
    t.index = ['Log return', 'Avg.  DD', 'Sharpe ratio', 'VaR', 'ES', 'MDD']
    t.columns = ['performance']
    return t.T
# ----------------------------------------------------------------------------


# function portfolio_risk
def portfolio_risk(data_corr, data_vol, data_ratio):
    import numpy as np
    array_corr = data_corr.to_numpy()
    array_vol = np.diag(data_vol)
    array_cov = np.dot(np.dot(array_vol, array_corr), array_vol)
    array_ratio = np.array(data_ratio)
    return np.sqrt(
        np.dot(np.dot(array_ratio, array_cov), array_ratio.transpose())
    )
# ----------------------------------------------------------------------------


# function period_4_plot
def period_4_plot(start, end, n):
    import pandas as pd
    df = pd.DataFrame([[start, n], [end, n]])
    df[0] = pd.to_datetime(df[0])
    df.set_index(0, drop=True, inplace=True)
    return(df)
# ----------------------------------------------------------------------------
