from os.path import join
import cPickle as pkl
import numpy as np

####################################################
# FUNCTION: Conditional_distribution
# 
# Initial Version for Debugging Only. Not being used
# in the project.
#
####################################################

#NOTE: DEPRECATED
def Conditional_distribution(part1,part2):
	gender = 'female'
	loaded = pkl.load(open(join('./pkls/',gender+'_PCA_coord_parameters.pkl')))
	
	data_part1 = loaded[part1]
	data_part2 = loaded[part2]
	mu1 = data_part1[-2]
	mu2 = data_part2[-2]
	sigma1 = data_part1[-1]
	sigma2 = data_part2[-1]
	data_part1 = data_part1[0:-2,:]
	no_rows1 = data_part1.shape[0]
	data_part1 = (data_part1-mu1).T
	data_part2 = data_part2[0:-2,:]
	no_rows2 = data_part2.shape[0]
	data_part2 = (data_part2-mu2).T
	
	sigma11 = ((data_part1).dot((data_part1).T))/(no_rows1)
	sigma22 = ((data_part2).dot((data_part2).T))/(no_rows2)
	
	sigma12 = ((data_part1).dot((data_part2).T))/(no_rows1)
	sigma21 = sigma12.T
	
	x2 = np.random.normal(mu2,sigma2);
	mu1_2 = mu1 + (sigma12.dot(np.linalg.pinv(sigma22))).dot((x2-mu2))
	sigma1_2 = sigma22 - (((sigma12).T).dot(np.linalg.pinv(sigma11))).dot(sigma12)
	sigma_conditional = np.sqrt(np.diag(sigma1_2))
	
	return [mu1_2,sigma_conditional];
