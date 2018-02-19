from os.path import join
import cPickle as pkl


####################################################
# File: Condense
# Contains functions to reduce the number of parts
# by merging some of them
#
####################################################

def condense_parts(labels):
	sub_parts={};
	sub_parts['head']=['neck']
	sub_parts['upperBody']=['leftShoulder','rightShoulder','spine2','spine1']
	sub_parts['rightArm']=['rightUpperArm','rightForeArm']
	sub_parts['rightHand']=['rightFingers']
	sub_parts['leftArm']=['leftUpperArm','leftForeArm']
	sub_parts['leftHand']=['leftFingers']
	sub_parts['lowerBody']=['global','spine']
	sub_parts['rightThigh']=['rightCalf']
	sub_parts['leftThigh']=['leftCalf']
	sub_parts['rightFoot']=['rightToes']
	sub_parts['leftFoot']=['leftToes']
	
	for key in sub_parts:
		labels = [key if x in sub_parts[key] else x for x in labels];
	
	with open('condensed_partnames_per_vertex.pkl','wb') as file_:
		pkl.dump(labels,file_);


#FUNCTION: EXTRACT_NEIGHBOURS
#Creates a dictionary of dictionary where the pair of keys define
#a relation between two neighbouring parts
def extract_neighbours():
	neighbourhood = {}
	neighbourhood['head'] = dict.fromkeys(['upperBody']);
	neighbourhood['leftHand'] = dict.fromkeys(['leftArm']);
	neighbourhood['leftArm'] = dict.fromkeys(['leftHand','upperBody']);
	neighbourhood['rightHand'] = dict.fromkeys(['rightArm']);
	neighbourhood['rightArm'] = dict.fromkeys(['rightHand','upperBody']);
	neighbourhood['leftFoot'] = dict.fromkeys(['leftThigh']);
	neighbourhood['leftThigh'] = dict.fromkeys(['leftFoot','lowerBody']);
	neighbourhood['rightFoot'] = dict.fromkeys(['rightThigh']);
	neighbourhood['rightThigh'] = dict.fromkeys(['rightFoot','lowerBody']);
	neighbourhood['lowerBody'] = dict.fromkeys(['upperBody','leftThigh','rightThigh']);
	neighbourhood['upperBody'] = dict.fromkeys(['lowerBody','head','leftArm','rightArm']);
	return neighbourhood;


#FUNCTIONS to save statistics of body parts
def SaveStats(accumulators,gender):
	with open(join('./custom/pkls/',gender+'_part_priors.pkl'),'wb') as file_:
		pkl.dump(accumulators,file_);

def SaveStats_coord(PCA_coord_matrix,gender):
	with open(join('./custom/pkls/',gender+'_PCA_coord_parameters.pkl'),'wb') as file_:
		pkl.dump(PCA_coord_matrix,file_);
