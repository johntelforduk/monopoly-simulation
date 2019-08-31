# A curried version of the Numpy percentile function.


from numpy import percentile


def curry_percentile(parm_percentile):
    def inner_func(parm_list):
        return percentile(parm_list, parm_percentile)
    return inner_func
