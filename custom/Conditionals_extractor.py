import cPickle as pkl
import numpy as np

#parent project headers
from smpl_utils import load_smpl
from time import sleep
from os.path import join

#Our Headers
from custom.DistributionManager import DistributionManager;
from custom.ConditionalDistribution import ConditionalDistribution;
from custom.condense import extract_neighbours


####################################################
#
# Function: SaveStats
# 
# Dumps the conditional distribution of neighbouring
# body parts on to the disk
#
# Params:
# @Conditionals: The dictionary of distribution
# @gender: male or female
#
####################################################
def SaveStats(conditionals,gender):
	with open('./custom/pkls/conditionals_neighbours_'+gender+'.pkl','wb') as file_:
		pkl.dump(conditionals,file_);

####################################################
#
# Function: Main
# Generates conditional Distribution of neighbouring
# parts From the provided data (after PCA).
#
####################################################
def main():
	gender = 'female'

	neighbourhood=extract_neighbours();				#get a dictionary of neighbourhood parts
	
	#load the PCA coordinates that were computed earlier
	loaded = pkl.load(open(join('./custom/pkls/',gender+'_PCA_coord_parameters.pkl')))
	
	Conditionals = {};								#dictionary to store conditional distributions
	distribution_manager= DistributionManager();	#See the file DistributionManager.py for details
	
	
	for parts in neighbourhood:						#iterate over all the body parts
		Conditionals[parts]={};					
		for neighbours in neighbourhood[parts]: 	#iterate over all it's neighbours	
			print parts, ' and ', neighbours;
			data_part1 = loaded[parts]
			data_part2 = loaded[neighbours]
			
			#Compute Conditional Distribution Parameters from the given data
			[sigma,pre_mew,mew1,mew2] = distribution_manager.GetDistribution(data_part1,data_part2);
			
			#Assign it to the conditional distribution dictionary
			Conditionals[parts][neighbours] = ConditionalDistribution(sigma,pre_mew,mew1,mew2);
	
	#Save the Dictionary
	SaveStats(Conditionals,gender);
	
main()
