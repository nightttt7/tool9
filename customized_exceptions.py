__all__ = ['DataFrameError', 'InputError', 'DateValueError',
           'UnfinishedFeature']


class DataFrameError(ValueError):
    pass


class InputError(ValueError):
    pass


class DateValueError(ValueError):
    pass


class UnfinishedFeature(FutureWarning):
    pass
