#!/usr/local/bin/ipython --gui=wx
from mayavi.mlab import triangular_mesh, figure
import numpy as np
from os.path import join
fig = figure()
data_path = './data/'
smpl_v = np.load(join(data_path,'verts.npy'))
verts = smpl_v.T
faces = np.load(join(data_path,'faces.npy'))
tm = triangular_mesh(verts[0], verts[1], verts[2], faces, color=(.7, .7, .9), figure=fig)
fig.scene.reset_zoom()
import ipdb; ipdb.set_trace()
