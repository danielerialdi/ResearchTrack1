from __future__ import print_function

import time
import timeit
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

total_counter = 0
""" number of tokens moved by the robot"""

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
    if(m not in token_array):
    	if(isinstance(m,int)):
    		token_array.append(m)
    
	
	
	
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
        	turn(10,0.2)
    
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
	
def diam_dist():
	array_all_token = []
	array_dist = []
	global token_array
	temp = True
	first = True
	markers = R.see()
	while(temp):
		turn(10,0.3)
		if(markers != R.see):
			markers = R.see()
			for m in markers:
				if(m.info.offset in array_all_token and first):
					first = False
					dist, index = min_dist()
				if(len(array_all_token) == len(token_array)):
					temp = False
					# print("FINAL")
				if(m.info.offset not in array_all_token):
					array_all_token.append(m.info.offset)
					array_dist.append(m.dist)
					update_token_array(m.info.offset)
				
			# print(array_all_token)
	i = array_dist.index(max(array_dist))
	# print(str(max(array_dist))+" "+ str(array_all_token[i]))
	return max(array_dist), array_all_token[i]
			
		
	
	
def first_iteration():
	global first_iteration_condition
	while not first_iteration_condition:
		dist, indexD = diam_dist()
		find_that_token(indexD)
		markers = R.see()
		for m in markers:
			update_token_array(m)
			if(dist-d_th<m.dist<dist+d_th):
				rot_y = m.centre.polar.rot_y
				while rot_y > a_th:
					if rot_y < -a_th: 
						print("Left a bit...")
						turn(-4, 0.3)
	    				elif rot_y > a_th:
						print("Right a bit...")
						turn(+4, 0.3)
					# print(rot_y)
					dist, rot_y = find_that_token(m.info.offset)
					if -a_th<rot_y < a_th:
						# print("Offset "+str(m.info.offset))
						first_iteration_condition = True
						break
	global token_array
	dist_max = max_dist()
	dist_min = min_dist()
	diameter = dist_max[0]-dist_min[0]
	# print(str(dist_min))
	for i in range(0,len(token_array)-1):
		#token_array.pop("dist_min[1]")
		if token_array[i] == dist_min[1]:
			token_array.pop(i)
	token_array.insert(0, dist_min[1])
	# print(token_array)
	global radius
	radius = diameter/2.0
	param = diameter
	while(param > radius):
		param, rot_y = find_that_token(indexD)
		dist_min = min_dist()
		param = param-dist_min[0]
		drive(20,0.1)
def main():
	markers = R.see()
	global token_array
	global total_counter
	instance = 0
	while_condition = 0
	second_iteration = 0
	avg = 0
	while 1:
	    dist, rot_y = find_token()
	    while (R.see() and while_condition == 0):
	    	marker = R.see()
		for m in markers:
			if(m.info.offset not in token_array):
		    		update_token_array(m.info.offset)
	    	turn(-10,1)
	    if(while_condition == 0):
	    	turn(10,1)
	    while(R.see() and while_condition == 0):
	    	marker = R.see()
		for m in markers:
			if(m.info.offset not in token_array):
		    		update_token_array(m.info.offset)
	    	turn(10,1)
	    while((not R.see()) and while_condition == 0):
	    	# print(str(R.see()))
	    	turn(30,1)
	    while_condition = 1
	    if not R.see() and total_counter == len(token_array):
		print("My work here is done!!")
		exit()
	    elif dist <d_th: 
		# print("Found it!")
		R.grab() # if we are close to the token, we grab it.
		# FIRST ITERATION ONLY:
		global radius
		if instance == 0:
			first_iteration()
			instance = 1
		else:
			dist, rot_y = find_that_token(token_array[0])
			threshold = 0.55
			while(dist > threshold):
				drive(10,0.3)
				dist, rot_y = find_that_token(token_array[0])
				if -a_th<= rot_y <= a_th: # if the robot is well aligned with the token, we go forward
				    print("Ah, here we are!.")
				    drive(20, 0.2)
	    			elif rot_y < -a_th:
				    print("Left a bit...")
				    turn(-4, 0.3)
	    			elif rot_y > a_th:
				    print("Right a bit...")
				    turn(+4, 0.3)
				# print(str(dist)+ " with token " +str(token_array[0]) )
				
		if(R.release()):
			R.release()
			total_counter = total_counter + 1
			# print("counter" + str(total_counter))
		drive(-20,1)
		if(second_iteration == 1):
			turn(-10,avg)
			# print(str(avg))
			while(not R.see() and total_counter != len(token_array)):
				turn(10,0.2)
				# print("CONDITION"+str(total_counter)+ " " +str(len(token_array)))
		if(second_iteration == 0):
			start_time = time.time()
			while(R.see() and second_iteration == 0):
				turn(-10,1)
			end_time = time.time()
			turn(10,1)
			avg = end_time-start_time-0.3
			# This is the time spent in the while loop - a thrashold
			# This is done cause we have to not consider the check in the while but just the turning
			# Even if we assume a time = 0 to check the condition of the while loop, the time calculated
			# is given for going further (in fact we have to come back to see the marker again)
			second_iteration = 1
			# print(str(avg))
		dist, rot_y = find_token()
		
			
	    elif -a_th<= rot_y <= a_th: # if the robot is well aligned with the token, we go forward
		print("Ah, here we are!.")
		drive(20, 0.2)
	    elif rot_y < -a_th: # if the robot is not well aligned with the token, we move it on the left or on the right
		print("Left a bit...")
		turn(-4, 0.3)
	    elif rot_y > a_th:
		print("Right a bit...")
		turn(+4, 0.3)
main()
