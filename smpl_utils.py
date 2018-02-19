# (c) 2016 Max Planck Society
# see accompanying LICENSE.txt file for licensing and contact information

"""
Author(s): Gerard Pons-Moll, Javier Romero

See LICENCE.txt for licensing and contact information.
"""

from smpl_webuser.serialization import load_model
## Load SMPL model (here we load the female model)
## Make sure path is correct
def load_smpl(gender='female'):
    from os.path import join
    path = '/home/alfred/smpl/models/'
    if gender == 'female': 
        fname_female = 'basicModel_f_lbs_10_207_0_v1.0.0.pkl'
        m = load_model(join(path, fname_female))
    else: 
        fname_male = 'basicmodel_m_lbs_10_207_0_v1.0.0.pkl'
        m = load_model(join(path, fname_male))
    return m

