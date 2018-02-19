import cPickle as pkl
import numpy as np

from solution.visualize_point_cloud import visualize_point_cloud
from smpl_utils import load_smpl
from os.path import join

#Our header files
from custom.Accumulator import DistributionAccumulator;
from custom.ConditionalDistribution import ConditionalDistribution;
from custom.condense import extract_neighbours


########################################################################
# FUNCTION: main
# Samples the body shapes from learned priors/conditionals
# 
# NOTE: You need to first execute the following files in order
#		1. Shape_dataset.py
#		2. Conditionals_Extractor.py
#
#
# Due to numerical instability in RightArm, there is a dirty
# IF-ELSE check that limits its number of iterations in Gibbs sampling
#
########################################################################
def main():

	#Basic Environment Setup
	gender='male'
	MAYAVI = True
	if not MAYAVI:
		from body.mesh.meshviewer import MeshViewers
		mv = MeshViewers(shape=[1,2])
	else:
		from mayavi.mlab import triangular_mesh, figure
		mv = figure(size=(800,800))
	
	smpl = load_smpl(gender=gender)
	tm = visualize_point_cloud(smpl.r, smpl.f, mv=mv)
	
	labels = pkl.load(open('./data/condensed_partnames_per_vertex.pkl'))				#Name of the body parts that we have
	indices = pkl.load(open('./custom/pkls/vertices_per_part.pkl'))						#A dictionary with key as body part name and value as list of part's vertices in the mesh
	priors = pkl.load(open(join('./custom/pkls/',gender+'_part_priors.pkl')))			#Dictionary containing PCA components and prior distribution for each body part
	pairwise = pkl.load(open('./custom/pkls/conditionals_neighbours_'+gender+'.pkl')) #A dictionary containing a sampler for conditioned gaussian distribution P(Part1|Part2)
	
	neighbourhood=extract_neighbours();													#defines the graph itself, which parts are neighbours of which part
	print("Set the view angle as desired in gui")
	import ipdb; ipdb.set_trace();

	samples=20;																			#How many body shapes would you like to generate?
	start_point='upperBody';															#Which body part should I start with?															#Set to true if neighbouring body parts should update each other in a cycle
	
	for sample_id in xrange(samples):													#generate body shapes one by one
		sampled_parts={};
		stack=[];
		
		verts = np.copy(smpl.r)
		faces = smpl.f
		
		root_ = priors[start_point].sample_raw(); 										#get the root first
		sampled_parts[start_point]=root_;												#sample it using its own prior
		stack.append(start_point);														#add it as the starting point for the algorithm
		
		#depth first graph traversal
		while(len(stack)!=0):															#traverse graph starting from the specified node
			curr_root = stack.pop(); 													#load the next item
			neighbours = neighbourhood[curr_root]; 										#get neighbours of the current body part
			for neighbour in neighbours:												#iterate over its neighbours now
				if neighbour not in sampled_parts:
					if gender=='female' and neighbour=='rightArm':
						iters=4;
					elif gender=='male' and neighbour=='leftArm':
						iters=100;
					else:
						iters=500;
					
					#sample the neighbour conditioned on the observed part i.e. curr_root
					sampled_parts[neighbour] = pairwise[neighbour][curr_root].getSample(sampled_parts[curr_root],iters);	
					print 'Assigned: ',neighbour
					stack.append(neighbour);							#add neighbour to explore its further neighbours
					#print 'Setting: ', neighbour,' to sampling queue' 
		
		#Assign to mesh
		for parts in sampled_parts:
			verts[indices[parts]]=priors[parts].get_global(sampled_parts[parts]);
		
		#display
		print 'Mesh Generated'
		visualize_point_cloud(verts, faces, mv=mv)
		import ipdb;ipdb.set_trace();
		
		

main()
