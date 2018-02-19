import numpy as np;

class AreaScore(object):
	
	def getScore(self,v1,v2,v3):
		
		s1 = np.linalg.norm(v1-v2);
		s2 = np.linalg.norm(v1-v3);
		s3 = np.linalg.norm(v3-v2);
		
		p = (s1+s2+s3)/2.0;
		
		area = np.sqrt( p* (p-s1) * (p-s2) * (p-s3) );
		
		return area;
		
class PerimeterScore(object):
	
	def getScore(self,v1,v2,v3):
		
		s1 = np.linalg.norm(v1-v2);
		s2 = np.linalg.norm(v1-v3);
		s3 = np.linalg.norm(v3-v2);
		
		return (s1+s2+s3);
