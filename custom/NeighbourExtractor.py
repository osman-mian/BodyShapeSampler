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
