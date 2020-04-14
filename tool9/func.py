__all__ = ['period', 'describe', 'ni', 'profit', 'sr', 'var', 'es', 'drawdown',
           'maxdrawdown', 'performance', 'portfolio_risk', 'period_4_plot']


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

# lr: log returns of protfolio, main input.
#     because of the characteristic of logarithm,
#     all the performances reflect the relatively performances in log returns,
#     but not absolute performances.
# most functions return a singgle number value

# function profit (sum log return)
def profit(lr):
    t = lr.sum()
    return t


# function sr (yearly sharpe ratio (no risk free rate) for returns)
# (not log returns here)
def sr(lr):
    import numpy as np
    s = lr.std()
    r = np.exp(lr)-1
    t = r.mean()/s*np.sqrt(252)
    return t


# function var (value at risk for log returns)
# with confindence level = level (default 0.95)
def var(lr, *level):
    import numpy as np
    n = int(np.ceil(lr.count()*level[0]))
    t = lr.sort_values(ascending=False)[n-1]
    return t


# function es (expected shortfall for log returns)
def es(lr, *level):
    import numpy as np
    n = int(np.ceil(lr.count()*level[0]))
    t = lr.sort_values(ascending=False)[n-1:].mean()
    return t


# function drawdown (cumulative log returns drawdown)
# attention: only this function returns a series
def drawdown(lr):
    clr = lr.cumsum()
    cummax = clr.cummax()
    t = clr-cummax
    return t


# function maxdrawdown (maximum cumulative log returns drawdown)
def maxdrawdown(lr):
    clr = lr.cumsum()
    cummax = clr.cummax()
    t = (clr-cummax).min()
    return t


# function performance (all the performances for log returns)
def performance(lr, level):
    import pandas as pd
    t = pd.DataFrame([profit(lr), sr(lr), var(lr, level), es(lr, level),
                      maxdrawdown(lr)])
    t.index = ['profit', 'sharpe ratio', 'VaR', 'ES', 'maxdrawdown']
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
