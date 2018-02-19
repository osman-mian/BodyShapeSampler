# (c) 2017 Max Planck Society
# see accompanying LICENSE.txt file for licensing and contact information

"""
Author(s): Gerard Pons-Moll

See LICENCE.txt for licensing and contact information.
"""

from solution.visualize_point_cloud import visualize_point_cloud
from smpl_utils import load_smpl
import numpy as np
from math import pi
from os.path import join
import chumpy as ch
from time import sleep

MAYAVI = True

gender = 'female'
if __name__ == '__main__':
    data_path =  './data/'
    if not MAYAVI:
        from body.mesh.meshviewer import MeshViewers
        mv = MeshViewers(shape=[1,2])
    else:
        from mayavi.mlab import triangular_mesh, figure
        mv = figure(size=(800,800))
    # smpl
    smpl = load_smpl(gender=gender)
    values = np.arange(-3, 3, 0.5)
    first_frame = True
    for beta in values:
        smpl.betas[0] = beta
        if first_frame: 
            tm = visualize_point_cloud(smpl.r, smpl.f, mv=mv)
            # Set the view angle as desired
            print("Set the view angle as desired in gui")
            import ipdb; ipdb.set_trace();
            first_frame = False
        else: 
            # update vertices only, not whole scene
            dummy = visualize_point_cloud(smpl.r, smpl.f, mv=mv, mlab_obj=tm)
            sleep(0.3)
            

