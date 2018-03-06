
# BodyShapeSampler

A sampler for body shape generation. Made as final project for Probablistic Graphical Models Course
This project is an extension to SMPL. We assume that you already have SMPL installed on your system. <br>
To download SMPL visit : http://smpl.is.tue.mpg.de/ (Please be sure to read the license agreement) 


###########################################################
Run scripts with 
ipython --gui=wx <name_of_script.py>

###########################################################

The following order should be used when training the new model:

First: cd to the SMPL folder

1. ipython --gui=wx shape_dataset.py  <br>
2. ipython --gui=wx ./custom/Conditionals_extractor.py <br>
3. ipython --gui=wx ./BodyShapeSampler.py  <br>


[1] will generate the priors. <br>
[2] will calculate conditionals<br>
[3] will sample body shapes. <br>


###########################################################################


Notes:

1. In all 3 files, you will have to specify the gender (male/female) for the sampler to work. <br>
2. In [3] you have the liberty to define a "starting point" in the code. The body will be sampled starting from this body part. <br>

