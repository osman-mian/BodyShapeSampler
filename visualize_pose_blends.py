# (c) 2017 Max Planck Society
# see accompanying LICENSE.txt file for licensing and contact information

"""
Author(s): Gerard Pons-Moll

See LICENCE.txt for licensing and contact information.
"""

from solution.visualize_point_cloud import visualize_point_cloud
from solution.visualize_two_point_clouds import visualize_two_point_clouds
from smpl_utils import load_smpl
import numpy as np
from os.path import join
import chumpy as ch
from time import sleep

MAYAVI = True

no_blend_weights = False
no_pose_blends = False
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
    all_samples = np.load(join(data_path, 'smpl_sample_poses_{0}.npy'.format(gender))) 
    trans = np.array([1.0,.0,.0]) 
    for p in all_samples:
        smpl.pose[:] = p
        visualize_point_cloud(smpl.v_posed.r, smpl.f, mv=mv)
        visualize_two_point_clouds(smpl.v_posed.r, smpl.r + trans, smpl.f, mv=mv)
        #raw_input()
        import ipdb; ipdb.set_trace(); 

