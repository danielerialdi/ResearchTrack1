from __future__ import print_function

import time
from sr.robot import *

a_th = 2.0
""" float: Threshold for the control of the orientation"""

d_th = 0.4
""" float: Threshold for the control of the linear distance"""

R = Robot()
""" instance of the class Robot"""

first_iteration_condition = False
""" condition for the first iteration to find the centre of the arena """

token_array = []
""" array with token offsets yet to move. 
The first element will be the token put in the centre first, 
that will be a reference for the other movements of the robot"""

token_array_moved = []
""" array with token offsets that were alredy moved in the arena"""

radius = 0
""" integer that will be modifed in the first iteration with the radius of the arena"""


def drive(speed, seconds):
    """
    Function for setting a linear velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
    """
    Function for setting an angular velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0
    
def update_token_array(m):
    """
    Function to update the array "token_array"
    """
    global token_array
    if not(m.info.offset in token_array):
    	token_array.append(m.info.offset)
    
	
	
	
def find_token():
    """
    Function to find the closest token

    Returns:
	dist (float): distance of the closest token (-1 if no token is detected)
	rot_y (float): angle between the robot and the token (-1 if no token is detected)
    """
    dist=100
    for token in R.see():
        if token.dist < dist:
            dist=token.dist
	    rot_y=token.rot_y
    if dist==100:
        return -1, -1
    else:
        return dist, rot_y
        
def find_token_from_list(array):
    """
    Function to find the closest token in a list of offsets

    Returns:
	dist (float): distance of the closest token (-1 if no token is detected)
	rot_y (float): angle between the robot and the token (-1 if no token is detected)
    """
    dist=100
    for token in R.see():
    	for i in range(1,len(array)-1): #1 because the first is the reference, could CHANGE
    		if token.info.offset == array[i]:
    			if token.dist < dist:
            			dist=token.dist
	    			rot_y=token.rot_y
	    			break
    if dist==100:
        return -1, -1
    else:
        return dist, rot_y

def find_that_token(m):
    """
    Function to find the chosen token

    Returns:
	dist (float): distance of the closest token (-1 if no token is detected)
	rot_y (float): angle between the robot and the token (-1 if no token is detected)
    """
    dist=100
    while dist == 100:
    	for token in R.see():
    		if(token.info.offset == m):
            		dist=token.dist
	    		rot_y=token.rot_y
    	if dist==100:
        	turn(5,0.5)
    
    return dist, rot_y
def min_dist():
	markers = R.see()
	min_dist = 100;
	for m in markers:
		if(m.dist < min_dist):
			min_dist = m.dist
			index = m.info.offset
	return min_dist, index

def max_dist():
	markers = R.see()
	max_dist = 0;
	for m in markers:	
		if(m.dist > max_dist):
			max_dist = m.dist
			index = m.info.offset
	return max_dist, index
def first_iteration():
	global first_iteration_condition
	while not first_iteration_condition:
		turn(-5, 0.5)
		dist, index = max_dist();
		result = "The dist is : " + str(dist) 
		print(result)
		# Can I assume to know this? It is only for the first iteration
		# to find the centre of the arena.
		if(dist > 5.0):
			markers = R.see()
			for m in markers:
				update_token_array(m)
				if(dist-d_th<m.dist<dist+d_th):
					rot_y = m.centre.polar.rot_y
					while rot_y > a_th:
						if rot_y < -a_th: 
							print("Left a bit...")
							turn(-2, 0.5)
	    					elif rot_y > a_th:
							print("Right a bit...")
							turn(+2, 0.5)
						print(rot_y)
						dist, rot_y = find_that_token(m.info.offset)
						if -a_th<rot_y < a_th:
							print("Offset "+str(m.info.offset))
							first_iteration_condition = True
							break
	global token_array
	print(str(token_array))
	dist_max = max_dist()
	dist_min = min_dist()
	diameter = dist_max[0]-dist_min[0]
	print(str(dist_min))
	for i in range(0,len(token_array)-1):
		#token_array.pop("dist_min[1]")
		if token_array[i] == dist_min[1]:
			token_array.pop(i)
	token_array.insert(0, dist_min[1])
	print(token_array)
	global radius
	radius = diameter/2.0
	param = diameter
	while(param > radius):
		param, rot_y = find_that_token(8)
		dist_min = min_dist()
		param = param-dist_min[0]
		drive(10,0.3)
def main():
	markers = R.see()
	time = 0
	#for m in markers:
		#rot_y = m.centre.polar.rot_y
		#print(str(rot_y))
    	#	if m.info.marker_type in (MARKER_TOKEN_GOLD, MARKER_TOKEN_SILVER, MARKER_ARENA):
        #		#print(" - Token {0} is {1} metres away".format( m.info.offset, m.dist ))
        #	elif m.info.marker_type == MARKER_ARENA:
        #		print(" - Arena marker {0} is {1} metres away".format( m.info.offset, m.dist ))
	while 1:
	    #if time == 0:
	    dist, rot_y = find_token()
	    	
	    #	dist, rot_y = find_token_from_list(token_array)
	    if dist==-1:
		print("I don't see any token!!")
		exit()  # if no markers are detected, the program ends
	    elif dist <d_th: 
		print("Found it!")
		R.grab() # if we are close to the token, we grab it.
		# FIRST ITERATION ONLY:
		global radius
		if time == 0:
			first_iteration()
			time = 1
		else:
			global token_array
			dist, rot_y = find_that_token(token_array[0])
			trashold = 0.6
			while(dist > trashold):
				drive(10,0.3)
				dist, rot_y = find_that_token(token_array[0])
				print(str(dist)+ " with token " +str(token_array[0]) )
				
		R.release()
		drive(-20,1)
		delta = 10.0
		turn(-20, 2)
		dist, rot_y = find_token()
		#while dist < radius:
		#	turn(5,1)
		#	print(rot_y)
		#	dist, rot_y = find_token()
			
	    elif -a_th<= rot_y <= a_th: # if the robot is well aligned with the token, we go forward
		print("Ah, here we are!.")
		drive(10, 0.5)
	    elif rot_y < -a_th: # if the robot is not well aligned with the token, we move it on the left or on the right
		print("Left a bit...")
		turn(-2, 0.5)
	    elif rot_y > a_th:
		print("Right a bit...")
		turn(+2, 0.5)
main()
    
