# -*- coding: utf-8 -*-
"""
[Python 2.7 (Mayavi is not yet compatible with Python 3+)]
Created on Tue Feb 10 18:27:17 2015
@author: Ryan Stauffer
https://github.com/ryanpstauffer/market-vis

Market Visualization Prototype 
Visualization and Interactive module
"""

import numpy as np
from mayavi import mlab
import datetime

def picker_callback(picker_obj):
    picked = picker_obj.actors
    if vis.actor.actor._vtk_obj in [o._vtk_obj for o in picked]:
        # m.mlab_source.points is the points array underlying the vtk
        # dataset. GetPointId return the index in this array.
        x_, y_ = np.lib.index_tricks.unravel_index(picker_obj.point_id,dims)
        print('Data indices: %i, %i' % (x_, y_))
        print(x[x_, y_], y[x_, y_], z[x_, y_] )
        cursor3d.mlab_source.set(x=x[x_, y_],
                                 y=y[x_, y_],
                                 z=z[x_, y_])