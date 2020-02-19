import numpy as np
import pandas as pd
from typing import Literal

class LensReferenceFrame:
    """Reference frame where x-axis is a lens symmetry axis.

    Args:
        center: origin of the frame.
        x_axis: direction of the x-axis.

    """

    hint_frame = Literal['barycenter', 'primary', 'secondary']

    def __init__(self, center: hint_frame = 'barycenter', x_axis: str = '12'):

        self.center = center
        self.x_axis = x_axis

    def to_frame(self, z: np.ndarray, new_frame: hint_frame, **kwargs):
        """Compute positions in a new reference frame.

        Args:
            z: position in old reference frame.
            new_frame: new reference frame.

        Keyword arguments:
            sep (float): separation
            titi (int): jj

        """
        z_new = pd.DataFrame()
        z_new['before'] = z
        z_new['after'] = z
        
        sep = kwargs['sep']
        gl1 = kwargs['gl1']
        x_offset = 0
        
        if not self.center == new_frame.center:
            if self.center == 'primary':
                if new_frame.center == 'secondary':
                    x_offset = sep
                if new_frame.center == 'barycenter':
                    x_offset = np.abs(gl1)

            if self.center == 'secondary':
                if (new_frame.center == 'primary'):
                    x_offset = - sep
                if (new_frame.center == 'barycenter'):
                    x_offset = - sep + np.abs(gl1)

            if self.center == 'barycenter':
                if (new_frame.center == 'primary'):
                    x_offset = - np.abs(gl1)
                if (new_frame.center == 'secondary'):
                    x_offset = sep - np.abs(gl1)
        
        if self.x_axis == new_frame.x_axis:
            if self.x_axis == '12':
                z_new['after'] = z_new['after'] - x_offset
            if self.x_axis == '21':
                z_new['after'] = z_new['after'] + x_offset

        else:
            z_new['after'] = - z_new['after'].values.conjugate()
            if self.x_axis == '12':
                z_new['after'] = z_new['after'] + x_offset

            if self.x_axis == '21':
                z_new['after'] = z_new['after'] - x_offset
        return z_new['after'].values
