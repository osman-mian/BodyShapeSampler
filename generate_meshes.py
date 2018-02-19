# (c) 2016 Max Planck Society
# see accompanying LICENSE.txt file for licensing and contact information

"""
Author(s): Gerard Pons-Moll, Javier Romero

See LICENCE.txt for licensing and contact information.
"""

from experiments.gerard.utils import data_paths
import numpy as np
from os.path import join
if __name__ == '__main__':
    save_path =  './data/'
    dp = data_paths(gender = 'male')
    smpl_v = dp.get_smpl()

    # Save the smpl mesh
    np.save(join(save_path,'verts.npy'),smpl_v.r)
    np.save(join(save_path,'faces.npy'),smpl_v.f)

    # Save two different shapes
    shape1 = smpl_v.pose_subjects[0]['v_template']
    shape2 = smpl_v.pose_subjects[8]['v_template']
    np.save(join(save_path,'shape1.npy'),shape1)
    np.save(join(save_path,'shape2.npy'),shape2)

    # Save two different poses
    p1 = smpl_v.pose_subjects[8]['pose_parms'][0]
    t1 = smpl_v.pose_subjects[8]['trans_parms'][0]
    p2 = smpl_v.pose_subjects[8]['pose_parms'][2]
    t2 = smpl_v.pose_subjects[8]['trans_parms'][2]
    smpl_v.pose[:] = p1
    smpl_v.trans[:] = t1
    dp.get_mesh(smpl_v.r).show()
    np.save(join(save_path,'pose1.npy'),smpl_v.r)
    smpl_v.pose[:] = p2
    #smpl_v.trans[:] = t2
    dp.get_mesh(smpl_v.r).show()
    np.save(join(save_path,'pose2.npy'),smpl_v.r)

    # Save two different shape and pose
    smpl_v = dp.get_smpl()
    np.save(join(save_path,'pose_shape1.npy'),smpl_v.r)
    dp.get_mesh(smpl_v.r).show()
    p3 = smpl_v.pose_subjects[0]['pose_parms'][1]
    t3 = smpl_v.pose_subjects[0]['trans_parms'][1]
    shape3 = smpl_v.pose_subjects[0]['v_template']
    smpl_v.pose[:] = p3
    #smpl_v.trans[:] = t3
    smpl_v.v_template[:] = shape3
    np.save(join(save_path,'pose_shape2.npy'),smpl_v.r)
    dp.get_mesh(smpl_v.r).show()
