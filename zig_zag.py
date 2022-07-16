"""
Zig Zag Indicator
"""

from typing import List, Dict, Any
import numpy as np


def zig_zag(high: np.ndarray, low: np.ndarray, point: float,
            depth: int, deviation:int, back_step: int) -> np.ndarray:

    extremum = 0 # searching for the first extremum
    peak     = 1 # searching for the next ZigZag peak
    bottom   =-1  # searching for the next ZigZag bottom

    ext_recalc = 3 # number of last extremes for recalculation

    i = 0
    start = 0
    extreme_counter = 0
    extreme_search = extremum
    shift = 0
    back = 0
    last_high_pos = 0
    last_low_pos = 0
    val = 0
    res = 0
    cur_low= 0
    cur_high = 0
    last_high=0
    last_low=0

    nrow = high.shape[0]
    rates_total = nrow

    vec_high = high
    vec_low = low

    # initializing
    vec_zig_zag = np.zeros((nrow,))
    vec_zig_zag_high = np.zeros((nrow,))
    vec_zig_zag_low = np.zeros((nrow,))
    start = depth

    if (nrow < 100):

        return vec_zig_zag

    # searching for the third extremum from the last uncompleted bar
    i = rates_total - 1

    while ((extreme_counter < ext_recalc) and (i > rates_total-100)):

        res = vec_zig_zag[i]

        if (res != 0.0):

            extreme_counter =+ 1

        i -= 1

    i += 1
    start = i

    # what type of exremum we search for
    if (vec_zig_zag_low[i] != 0.0):

        cur_low = vec_zig_zag_low[i]
        extreme_search = peak

    else:

        cur_high = vec_zig_zag_high[i]
        extreme_search = bottom

    # clear indicator values

    vec_zig_zag[start+1:rates_total] = 0.0
    vec_zig_zag_low[start+1:rates_total] = 0.0
    vec_zig_zag_high[start+1:rates_total] = 0.0

    # searching for high and low extremes
    
    for shift in np.arange(start, rates_total):

        # low
        val = low[lowest(vec_low, depth, shift)]

        if (val == last_low):

            val = 0.0

        else:

            last_low = val

            if ((low[shift] - val) > (deviation * point)):

                val=0.0

            else:

                for back in np.arange(1, back_step):

                    res = vec_zig_zag_low[shift-back]

                    if ((res != 0) and (res > val)):

                        vec_zig_zag_low[shift-back] = 0.0

        if (low[shift] == val):

            vec_zig_zag_low[shift] = val

        else:

            vec_zig_zag_low[shift] = 0.0

        # high
        val = high[highest(vec_high, depth, shift)]

        if (val == last_high):

            val=0.0;

        else:

            last_high = val

            if ((val - high[shift]) > (deviation * point)):

                val=0.0

            else:

                for back in np.arange(1, back_step):

                    res = vec_zig_zag_high[shift-back]

                    if ((res != 0) and (res < val)):

                        vec_zig_zag_high[shift-back]=0.0

        if (high[shift] == val):

            vec_zig_zag_high[shift] = val

        else:

            vec_zig_zag_high[shift] = 0.0

    # set last values
    if (extreme_search == 0): # undefined values

        last_low = 0.0
        last_high = 0.0

    else:

        last_low = cur_low
        last_high = cur_high

    # final selection of extreme points for ZigZag
    
    for shift in np.arange(start, rates_total):

        res = 0.0

        if extreme_search == extremum:

            if ((last_low==0.0) and (last_high==0.0)):

                if (vec_zig_zag_high[shift] != 0.0):

                    last_high = high[shift]
                    last_high_pos = shift
                    extreme_search = bottom;
                    vec_zig_zag[shift] = last_high
                    res = 1

                if (vec_zig_zag_low[shift] != 0.0):

                    last_low = low[shift]
                    last_low_pos = shift
                    extreme_search = peak
                    vec_zig_zag[shift] = last_low
                    res = 1

        elif extreme_search == peak:

            if ((vec_zig_zag_low[shift] != 0.0) and
                (vec_zig_zag_low[shift] < last_low) and
                (vec_zig_zag_high[shift] == 0.0)):

                vec_zig_zag[last_low_pos] = 0.0
                last_low_pos = shift
                last_low = vec_zig_zag_low[shift]
                vec_zig_zag[shift] = last_low
                res = 1

            if ((vec_zig_zag_high[shift] != 0.0) and
                (vec_zig_zag_low[shift] == 0.0)):

               last_high = vec_zig_zag_high[shift]
               last_high_pos = shift
               vec_zig_zag[shift] = last_high
               extreme_search = bottom
               res = 1

        elif extreme_search == bottom:

            if ((vec_zig_zag_high[shift] != 0.0) and
                (vec_zig_zag_high[shift] > last_high) and
                (vec_zig_zag_low[shift] == 0.0)):

                vec_zig_zag[last_high_pos] = 0.0
                last_high_pos = shift
                last_high = vec_zig_zag_high[shift]
                vec_zig_zag[shift] = last_high

            if ((vec_zig_zag_low[shift] != 0.0) and
                (vec_zig_zag_high[shift] == 0.0)):

               last_low = vec_zig_zag_low[shift]
               last_low_pos = shift
               vec_zig_zag[shift] = last_low
               extreme_search = peak

        else:

            return vec_zig_zag

    return vec_zig_zag


def highest(array: np.ndarray, depth: int, start: int):

    if start < 0:

        return 0

    else:

        idx_max = array[start-depth:start-1].argmax()

        return idx_max


def lowest(array: np.ndarray, depth: int, start: int):

    if start < 0:

        return 0

    else:

        idx_min = array[start-depth:start-1].argmin()

        return idx_min
