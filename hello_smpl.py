from smpl_utils import load_smpl
from mayavi.mlab import figure
from solution.visualize_point_cloud import visualize_point_cloud
import numpy as np
from time import sleep
gender = 'female'

# Load SMPL
smpl = load_smpl(gender=gender)
smpl1 = load_smpl(gender=gender)
smpl2 = load_smpl(gender='male')

# Create a figure
mv = figure(size=(800, 600))

# Visualize the average template
vals = np.arange(0, 1, 0.1)
first = True
for val in vals:
    half = smpl.v_template.r.shape[0]/2
    smpl.v_template[:200,:] = (1 + val)* smpl1.v_template.r[:200,:]
    smpl.v_template[half:half+200,:] = (1 + val)* smpl1.v_template.r[half:half+200,:]
    if first:
        first_mod = visualize_point_cloud(smpl.r, smpl.f, mv=mv)
        first = False
        sleep(0.5)
    else:
        visualize_point_cloud(smpl.r, smpl.f, mv=mv, mlab_obj=first_mod)
        sleep(0.3)


