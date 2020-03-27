__all__ = ['RRP']


from datetime import timedelta
import pandas as pd
from pandas.api.types import is_datetime64_any_dtype
import numpy as np
from .func import portfolio_risk, period, es
from .customized_exceptions import (DataFrameError, InputError, DateValueError,
                                    UnfinishedFeature)


class RRP(object):
    """ construct a risk parity portfolio

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
        ratio_fixed: list, a fixed ratio of assets, !!construct FRP if provided
        logr: log return of assets, pd.DataFrame with column be asset name,
            index be datetime
        risk: risk of assets, pd.DataFrame with column name be risk name,
            index be datetime
        corr: correlation between assets for each observation, pd.DataFrame
            with column name be asset name, outer index be datetime, inner
            index be asset name
        first_reset_date: string or datetime, reset at the begining of day
        reset_months: int, number of months between two reset date
        reset_shift_mode: determine whether take the first trading day after or
            before the planed reset date as real reset date
        target_risk: int, if target_risk is provided, the leverage of portfolio
            will be set so that portfolio risk will equal to the target_risk
        leverage_fixed: number, !!if provided, the leverage of portfolio will
            not change and always be it
        leverage_limit: number, if provided, leverage won't be higher than it
        get_actual: default False, get actual ratio, portfolio risk and actual
            portfolio risk

        [output]
        sample_month_interval: total months in sample period
        reset_times: times of reset
        reset_date: pd.DatetimeIndex, the date of reset dates
        logr_p: portfolio log return, pd.DataFrame with column name be asset
            name, index be datetime
        ratio: retio of assets, pd.DataFrame with column name be asset name,
            index be datetime
        ratio_actual: actual ratio of assets, pd.DataFrame with column name be
            asset name, index be datetime
        risk_p: portfolio risk, pd.DataFrame with column name be 'portfolio',
            index be datetime
        risk_p_actual: actual portfolio risk, pd.DataFrame with column name be
            'portfolio', index be datetime
        leverage: leverage of portfolio, pd.DataFrame with column name be
            'leverage', index be datetime
    """

    def __init__(self, **kw):
        if not kw:
            raise InputError('please provide arguments, please')
        # inputs
        self.ratio_fixed = None
        self.logr = None
        self.risk = None
        self.corr = None
        self.first_reset_date = None
        self.reset_months = 12
        self.reset_shift_mode = 'after'
        self.target_risk = None
        self.leverage_fixed = None
        self.leverage_limit = None
        self.get_actual = False
        # generated useful values
        self.index = None
        self.first_day = None
        self.last_day = None
        self.N = None
        self.logr_names = None
        # outputs
        self.sample_month_interval = None
        self.reset_times = None
        self.reset_date = None
        self.logr_p = None
        self.ratio = None
        self.ratio_actual = None
        self.risk_p = None
        self.risk_p_actual = None
        self.leverage = None
        # do it
        self.input(kw)
        self.check_inputs()
        self.useful_data()
        self.construct()

    def input(self, kw):
        if 'ratio_fixed' in kw:
            self.ratio_fixed = kw['ratio_fixed']
        if 'logr' in kw:
            self.logr = kw['logr']
        else:
            raise InputError('you muse input "logr"')
        if 'risk' in kw:
            self.risk = kw['risk']
        if 'corr' in kw:
            self.corr = kw['corr']
        if 'first_reset_date' in kw:
            self.first_reset_date = kw['first_reset_date']
        else:
            self.first_reset_date = self.logr.index[0]
        if 'reset_months' in kw:
            self.reset_months = kw['reset_months']
        else:
            raise InputError('you muse input "reset_months"')
        if 'reset_shift_mode' in kw:
            self.reset_shift_mode = kw['reset_shift_mode']
        if 'target_risk' in kw:
            self.target_risk = kw['target_risk']
        if 'leverage_fixed' in kw:
            self.leverage_fixed = kw['leverage_fixed']
        if 'leverage_limit' in kw:
            self.leverage_limit = kw['leverage_limit']
        if 'get_actual' in kw:
            self.get_actual = kw['get_actual']

    def check_inputs(self):
        if len(self.logr) != len(self.risk):
            raise DataFrameError('"logr" and "risk" have different length')
        if self.logr.shape[1] < 2:
            raise DataFrameError('"logr" must have more than 2 columns')
        if self.risk.shape[1] < 2:
            raise DataFrameError('"risk" must have more than 2 columns')
        if self.logr.shape[1] != self.risk.shape[1]:
            raise DataFrameError('"logr" and "risk" have different col number')
        if not is_datetime64_any_dtype(self.logr.index):
            raise DataFrameError('the index of "logr" is not datetime')
        if not is_datetime64_any_dtype(self.risk.index):
            raise DataFrameError('the index of "risk" is not datetime')
        if (self.logr.index != self.risk.index).sum():
            raise DataFrameError('"logr" and "risk" have different index')
        # FIXME: is_datetime64_any_dtype(timestamp) is False
        # if not (isinstance(self.first_reset_date, str) or
        #         is_datetime64_any_dtype(self.first_reset_date)):
        #     print('warning: "first_reset_date" should be string/datetime')
        if isinstance(self.first_reset_date, str):
            self.first_reset_date = pd.to_datetime(self.first_reset_date)
        if self.first_reset_date < self.logr.index[0]:
            raise DateValueError(
                'the "first_reset_date" must be earlier than the first day'
            )
        if not isinstance(self.reset_months, int):
            raise ValueError('"reset_months" should be int')
        # TODO: add check for lenth of corr

    def useful_data(self):
        self.index = self.logr.index
        self.first_day = self.index[0]
        self.last_day = self.index[-1]
        self.N = len(self.index)
        self.logr_names = list(self.logr.columns)

    def construct(self):
        self.get_sample_month_interval()
        self.get_reset_points()
        self.get_reset_date()
        self.get_last_reset_date()
        self.get_ratio()
        self.get_leverage()
        self.get_logr_p()
        if self.get_actual:
            self.get_ratio_actual()
            self.get_risk_p()
            self.get_risk_p_actual()
        else:
            self.ratio_actual = None
            self.risk_p = None
            self.risk_p_actual = None

    def new_ratio_fixed(self, change):
        self.ratio_fixed = change
        self.check_inputs()
        self.useful_data()
        self.construct()

    def new_logr(self, change):
        self.logr = change
        self.check_inputs()
        self.useful_data()
        self.construct()

    def new_risk(self, change):
        self.risk = change
        self.check_inputs()
        self.useful_data()
        self.construct()

    def new_corr(self, change):
        self.corr = change
        self.check_inputs()
        self.useful_data()
        self.construct()

    def new_first_reset_date(self, change):
        self.first_reset_date = change
        self.check_inputs()
        self.useful_data()
        self.construct()

    def new_reset_months(self, change):
        self.reset_months = change
        self.check_inputs()
        self.useful_data()
        self.construct()

    def new_reset_shift_mode(self, change):
        self.reset_shift_mode = change
        self.check_inputs()
        self.useful_data()
        self.construct()

    def new_target_risk(self, change):
        self.target_risk = change
        self.check_inputs()
        self.useful_data()
        self.construct()

    def new_leverage_fixed(self, change):
        self.leverage_fixed = change
        self.check_inputs()
        self.useful_data()
        self.construct()

    def new_leverage_limit(self, change):
        self.leverage_limit = change
        self.check_inputs()
        self.useful_data()
        self.construct()

    def new_get_actual(self, change):
        self.get_actual = change
        self.check_inputs()
        self.useful_data()
        self.construct()

    @staticmethod
    def month_interval(date1, date2):
        """
        function month_interval
        date2 should be after date1
        if day2 < day1, one month will be deducted
        """
        if date1 >= date2:
            raise ValueError('date2 should be after date1')
        year1 = date1.year
        year2 = date2.year
        month1 = date1.month
        month2 = date2.month
        day1 = date1.day
        day2 = date2.day
        return (year2-year1)*12 + (month2-month1) - (day2 < day1)

    def get_sample_month_interval(self):
        self.sample_month_interval = self.month_interval(self.first_reset_date,
                                                         self.last_day)

    def get_reset_points(self):
        reset_times = ((self.sample_month_interval) // self.reset_months
                       + 1)
        reset_points = (pd.date_range(
            start=(self.first_reset_date-timedelta(days=(self.first_reset_date.
                                                         day-1))),
            periods=reset_times, freq='{}MS'.format(self.reset_months)
        ) + timedelta(days=(self.first_reset_date.day-1)))
        self.__reset_points = reset_points
        self.reset_times = reset_times

    def get_reset_date(self):
        """
        if a reset point is a trading day, take it as reset_date
        else take the first trading day after(before) the reset
        point as reset_date
        also add the first_day as the first actual reset date
        """
        reset_points = self.__reset_points
        reset_date_list = list(range(self.reset_times))
        for i in range(len(reset_points)):
            day_diff = self.index - reset_points[i]
            # 'after' mode
            if self.reset_shift_mode in ('after', 'a', 'front', 'f'):
                day_shift = day_diff[day_diff >= timedelta(days=0)].min()
            # 'before' mode
            if self.reset_shift_mode in ('before', 'back', 'b'):
                day_shift = day_diff[day_diff <= timedelta(days=0)].max()
            reset_date_list[i] = reset_points[i] + day_shift
        if self.first_day != self.first_reset_date:
            reset_date_list.insert(0, self.first_day)
        self.reset_date = pd.DatetimeIndex(reset_date_list)

    def get_last_reset_date(self):
        """
        last_reset_date: DataFrame of the last reset date for each trade day
        NB! use reset_date but not last_reset_date sometimes is for
        faster calculations
        """
        last_reset_date = pd.DataFrame(index=self.index)
        last_reset_date.loc[self.reset_date, 'last_reset_date'] = \
            list(self.reset_date)
        last_reset_date.ffill(inplace=True)
        self.__last_reset_date = last_reset_date

    def get_ratio(self):
        ratio = pd.DataFrame(index=self.index)
        # fixed ration portfolio
        if self.ratio_fixed:
            i = 0
            for name in self.logr_names:
                ratio[name] = self.ratio_fixed[i]
                i = i + 1
        # risk parity portfolio
        else:
            # TODO: get ratio_reset for cases that number of assets more than 2
            if len(self.logr_names) == 2:
                ratio_reset = (self.risk.loc[self.reset_date, ].
                               apply(lambda x: (1/x) / (1/x).sum(), axis=1))
            elif len(self.logr_names) > 2:
                raise UnfinishedFeature(
                    'unfinished for cases that number of assets more than 2'
                )
            i = 0
            for name in self.logr_names:
                ratio[name] = np.NaN
                ratio.loc[self.reset_date, name] = ratio_reset.iloc[:, i]
                ratio.ffill(inplace=True)
                i = i + 1
        self.ratio = ratio

    def get_leverage(self):
        leverage = pd.DataFrame(index=self.index)
        if self.leverage_fixed:
            leverage['leverage'] = self.leverage_fixed
        elif self.target_risk:
            leverage['leverage'] = np.NaN
            for a_reset_date in self.reset_date:
                leverage.loc[a_reset_date] = self.target_risk / (
                    portfolio_risk(data_corr=self.corr.loc[a_reset_date],
                                   data_vol=self.risk.loc[a_reset_date],
                                   data_ratio=self.ratio.loc[a_reset_date])
                )
            leverage.ffill(inplace=True)
        else:
            leverage['leverage'] = 1
        if self.leverage_limit:
            leverage.loc[leverage['leverage'] > self.leverage_limit] = (
                self.leverage_limit
            )
        self.leverage = leverage

    def get_logr_p(self):
        leverage_tmp = pd.DataFrame(index=self.index)
        for name in self.logr_names:
            leverage_tmp[name] = self.leverage['leverage']
        # get actual cumulative assets return in one reset period
        # actual means ratio and leverage are used,
        # not the original return assets
        logr_with_last_reset_date = self.logr.copy()
        logr_with_last_reset_date['last_reset_date'] = self.__last_reset_date
        logr_cum = logr_with_last_reset_date.groupby('last_reset_date'). \
            cumsum()
        r_actual_cum = (np.exp(logr_cum)-1)*self.ratio*leverage_tmp
        # check if out of money
        if (r_actual_cum.sum(axis=1) < -1).sum() > 0:
            raise ValueError(
                'one asset out of money, please reduce leverage or set a limit'
            )
        # get cumulative portfolio log return in one reset period
        logr_p_cum = np.log(r_actual_cum.sum(axis=1)+1)
        # portfolio log return
        logr_p = pd.DataFrame(index=self.index)
        # for not on reset date
        logr_p.loc[:, 'portfolio'] = logr_p_cum.diff()
        # for on reset date, cover the value above
        logr_p.loc[self.reset_date, 'portfolio'] = \
            logr_p_cum.loc[self.reset_date]
        self.logr_p = logr_p
        self.__r_actual_cum = r_actual_cum

    def get_ratio_actual(self):
        ratio_actual_no_adjust = (self.__r_actual_cum+1)*self.ratio
        ratio_actual = ratio_actual_no_adjust.apply(lambda x: x / x.sum(),
                                                    axis=1)
        # if ratio_actual have any negative value at one date,
        # the ratio is meaningless, treat this date as missing value
        ratio_actual.loc[(ratio_actual < 0).sum(axis=1) > 0] = np.NaN
        self.ratio_actual = ratio_actual

    def get_risk_p(self):
        """
        difference: use ratio
        """
        risk_p = pd.DataFrame(index=self.index)
        risk_p['portfolio'] = np.NaN
        for a_reset_date in self.reset_date:
            risk_p.loc[a_reset_date] = (
                portfolio_risk(data_corr=self.corr.loc[a_reset_date],
                               data_vol=self.risk.loc[a_reset_date],
                               data_ratio=self.ratio.loc[a_reset_date])
            )
        risk_p.ffill(inplace=True)
        self.risk_p = risk_p

    def get_risk_p_actual(self):
        """
        difference: use ratio_actual
        """
        risk_p_actual = pd.DataFrame(index=self.index)
        risk_p_actual['portfolio'] = np.NaN
        for a_date in self.index:
            risk_p_actual.loc[a_date] = (
                portfolio_risk(data_corr=self.corr.loc[a_date],
                               data_vol=self.risk.loc[a_date],
                               data_ratio=self.ratio_actual.loc[a_date])
            )
        self.risk_p_actual = risk_p_actual

    def __str__(self):
        info = ('the construction of portfolio finished, useful attributes: ' +
                '\n sample_month_interval, ' +
                '\n reset_times, ' +
                '\n reset_date, ' +
                '\n logr_p, ' +
                '\n ratio, ' +
                '\n ratio_actual, ' +
                '\n risk_p, ' +
                '\n risk_p_actual, ' +
                '\n leverage'
                )
        return info

    __repr__ = __str__
