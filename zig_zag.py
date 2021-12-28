"""
Zig Zag Indicator
"""

from typing import List, Dict, Any
import numpy as np


def zig_zag(mat_ohlc: np.ndarray,
            depth: int, deviation:int, back_step:int) -> np.ndarray:

    ext_level = 3

    nrow = mat_ohlc.shape[0]

    mat_zig_zag = np.zeros((nrow, 3))
    vec_high = mat_ohlc[:, 1]
    vec_low = mat_ohlc[:, 2]

    if ((nrow < depth) or (back_step >= depth)):

        return(mat_zig_zag);


    # find first extremum in the depth ExtLevel or 100 last bars
    i = counter_z = 0

    while ((counter_z < ext_level) and (i < 100)):

        if (mat_zig_zag[i, 0] != 0.0):

            counter_z += 1

        i += 1

    # no extremum found - recounting all from begin
    if (counter_z == 0):

        limit = NRow - InpDepth;
        std::fill(matZigZag.begin(), matZigZag.end(), 0.0);

  } else {
      //--- set start position to found extremum position
      limit = i - 1;

      //--- what kind of extremum?
      if (matZigZag(i, 2) != 0.0) {

          //--- low extremum
          curlow = matZigZag(i, 2);

          //--- will look for the next high extremum
          whatlookfor = 1;

      } else {

          //--- high extremum
          curhigh = matZigZag(i, 1);

          //--- will look for the next low extremum
          whatlookfor = -1;
      }

      //--- clear the rest data
      for (i = limit-1; i >= 0; i--) {

          matZigZag(i, 0) = 0.0;
          matZigZag(i, 1) = 0.0;
          matZigZag(i, 2) = 0.0;
      }
  }

    return mat_zig_zag