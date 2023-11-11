# ResearchTrack1 - Assignment 1

## Table of contents

- [The objective of the assignment](https://github.com/danielerialdi/ResearchTrack1/master/README.md#the-objective-of-the-assignment)
- [How to run the program](https://github.com/danielerialdi/ResearchTrack1/master/README.md#how-to-run-the-program)
- [The assumptions](https://github.com/danielerialdi/ResearchTrack1/master/README.md#the-assumptions)
- [Possible strategies](https://github.com/danielerialdi/ResearchTrack1/master/README.md#possible-strategies)
- [How the script works](https://github.com/danielerialdi/ResearchTrack1/master/README.md#how-the-script-works)
  - [The first step](https://github.com/danielerialdi/ResearchTrack1/master/README.md#The-first-step)
  - [The other markers](https://github.com/danielerialdi/ResearchTrack1/master/README.md#The-other-markers)
- [Global variables in the code](https://github.com/danielerialdi/ResearchTrack1/master/README.md#Global-variables-in-the-code)
- [Functions in the code](https://github.com/danielerialdi/ResearchTrack1/master/README.md#Functions-in-the-code)
  - [Pseudocode for diam_dist](https://github.com/danielerialdi/ResearchTrack1/master/README.md#Pseudocode-for-diam_dist)
  - [Pseudocode for first_iteration](https://github.com/danielerialdi/ResearchTrack1/master/README.md#Pseudocode-for-first_iteration)
- [Pseudocode of the main function of the program](https://github.com/danielerialdi/ResearchTrack1/master/README.md#Pseudocode-of-the-main-function-of-the-program)


## The objective of the assignment
We have been given a simulator that is able to simulate a robot in a 2D environment and make it move around the arena and interact with the objects (markers) in it.
The robot is able to identify the markers in its field of view and identify the distance and the angle between the position of itself and the one of the object detected. 
The request is to program the robot to put the markers present in the arena close to each other, performing it with the minimum possible movements done by it.
## How to run the program
To be able to run the program it is necessary to pass to 'run.py' the filename of the script, while being in the right folder, as it follows:
```bash
$ python2 run.py assignment.py
```
## The assumptions
The ony assumption I made to write the program is that all markers are placed in a circle in the arena. 
I do not know the initial position of the robot nor the absolute position of the marker.
## Possible strategies
To be able to put all the markers close to each other, I could place all of them next to the one taken as reference; this would have meant to move all the markers except one (in this case 5) to an edge of the arena. This would have been easier to compute, but the robot would have spent more time moving around the arena. 
So the other possibility was to identify the centre of the arena and bring all the markers there; this requires an analisys prior to the beginning of the displacements of the markers, but the robot has to move as little as possible to reach the requirement of the assignment. 
## How the script works
The chosen alternative between the ones presented was the second one: bring all the markers in the centre of the arena.
### The first step
To identify the centre of the arena I use the only assumption I have made.
The first step is scanning with a rotation of 360 degrees on the starting position every marker I have near the robot. Then I proceed to go to the nearest marker, and do a second rotation. Doing this I save all the ids of the markers in an array, saving the distances as well. The marker with the longest distance from the robot is the one that I choose as target. The line which starts from the robot position and ends to the position of the marker, passes through the centre of the arena.
To calculate the radius I subtract to the distance from the farther marker with the one I have taken (that is the minimun distance) and dividing this by 2.
Then I drive forward until I have driven one radius length and I stop, realeasing the marker. This is the target I take as reference for all the other markers I will bring to the centre from now on, and it will be easily found beacause I cached its id position in the first index of the array containing all token's id (token_array).
### The other markers
Once I have set the first token in the middle of the arena, I drive backwards a little to make sure not to hit the object just released and I make the robot turn until I do not see any token in the field of view. When this occurs, I can turn back for an instance to have a token in my visual range, that will be the one I will grab next. It is now possible to analize the distance and the angle of the marker with respect to the robot; I can now let the robot drive towards it.
When the robot arrives at the destination grabs the token, and while it does not see the reference marker (the one put in the middle), turns. Then it will drive towards it and when it arrives at a certain threshold it will stop, releasing the maker. 
## Global variables in the code
| Variable | Constant | Meaning |
| -------- | -------- | -------- |
| a_th | Yes | Float variable, it is the threshold for the control of the orientation. It is set to 2.0 |
| d_th | Yes | Float variable, it is the threshold for the control of the linear distance. It is set to 0.4 |
| first_iteration_condition | No | Condition for the first iteration to find the centre of the arena |
| token_array | No | Array with token offsets. The first element will be the token put in the centre first, that will be a reference for the other movements of the robot |
| total_counter | No | Number of tokens moved by the robot |
| radius | No | Integer that will be modifed in the first iteration with the radius of the arena |
## Functions in the code
There are several functions used in the script code, some of them are from the libraries of the robot while some others were written to ease off some operations and to make the code more readable and understandable.
In the table that follows, all the functions written by myself are grouped and explained:
| Function | The purpose |
| -------- | -------- |
| drive(speed, seconds) | Sets a linear velocity for the robot with the first parameter and with 'seconds' it imposes to keep that velocity for a certain amount of time. |
| turn(speed,seconds) | It is similar to the drive function, but sets an angular velocity, instead of a linear one. |
| update_token_array(m) | Appends the offset of a marker seen for the first time by the robot to the array 'token_array' that is an array devolved to this duty. It checks if the offset is not already present in the array and that 'm' is a value of type int; only if those conditions are satisfied, it will append the object to the array.|
| find_token() | Finds the closest token between the ones that the robot has in its range of view. Returns the distance and the angle from the closest token. If no token is detected returns -1 for both the distance and the angle. |
| find_that_token(m)| Checks all the tokens that the robot sees in its range of view. If the wanted token is present, recognizable by the offset 'm' passed as argument, it returns the distance and the angle. If the robot cannot see the wanted token, it turns on itself a little and repeats the operation. |
| min_dist() | Compares the distance between the markers in the robot's range of view and returns the smallest distance and the index of the corresponding marker. |
| max_dist() | Compares the distance between the markers in the robot's range of view and returns the biggest distance and the index of the corresponding marker. |
| diam_dist() | Computes the maximum distance between all tokens and returns it with the offset which corresponds to it. The pseudocode follows to understand better how the function works. |
| first_iteration() | Computes the centre of the arena and guides the robot there. It does not return anything, it is only needed to make the code more readable. The pseudocode for this function is presented later. |

### Pseudocode for diam_dist
```
declare array_all_token empty  
declare array_dist empty  
declare first True  
declare temp True  
markers = markers that the robot sees  
while (temp is True):  
    turn_right  
    if (markers are different from the ones the root is seeing):  
        markers = markers that the robot sees  
        for (every markers m in the list of the ones the robot sees):  
            if((the offset of m is present in 'array_all_token') and (first is True)):  
                set first to False  
                dist, index = min_dist()  
             if(the length of array_all_token is equal to the length of token_array):  
                 set temp to False
             if(the offset of m is not present in 'array_all_token'):
                 append to array_all_token the offset of m
                 append to array_dist the distance of m
                 update_token_array(offset of m)
i = index of the maximum in array_dist
return (maximum in array_dist), array_all_token[i] 
```

### Pseudocode for first_iteration
```
while(first_iteration_condition is False):
    dist, indexD = diam_dist()  
    find_that_token(indexD)  
    markers = markers that the robot sees
    for (every markers m in the list of the ones the robot sees):
        update_token_array(m)
        if((distance of m) is in between (dist - d_th) and (dist + d_th)):
            rot_y = angle of m
            while(rot_y is greater that -a_th):
                if(rot_y is less than -a_th):
                    turn_left
                elif(rot_y is greater than a_th):
                    turn_right
                dist, rot_y = find_that_token(offset of m)
                if(rot_y is in between -a_th and a_th):
                    set first_iteration_condition to True
                    break
dist_max = max_dist()
dist_min = min_dist()
diameter = dist_max[0]-dist_min[0] # [0] is only the distance
for (every i in range 0, (length of token_array - 1)):
    if(token_array[i] is equal to dist_min[1]):
        pop i element in token_array
insert dist_min[1] in token_array in position 0
set radius to (diameter/2.0)
set param to diameter
while(param is greater than radius):
    param, rot_y = find_that_token(indexD)
    set dist_min to min_dist()
    set param to param-dist_min[0]
    drive
```
## Pseudocode of the main function of the program
```
markers = markers that the robot sees
set instance to 0
set while_condition to 0
set second_iteration to 0
set avg to 0
while True:
    dist, rot_y = find_token()
    # All this part is done to make the robot rotates on itself just at the beginning
    while (R.see() returns something and while_condition is equal to 0):
        marker = markers that the robot sees
        for (every markers m in the list of the ones the robot sees):
            if(offset of the marker m is not in token_array):
                update_token_array(offset of the marker m)
        turn_left
    if(while_condition is equal to 0):
        turn_right
    while(R.see() returns something and while_condition is equal to 0):
        marker = markers that the robot sees
		for (every markers m in the list of the ones the robot sees):
			if(offset of the marker m is not in token_array):
                update_token_array(offset of the marker m)
        turn_right
    while((R.see() does not return anything) and while_condition is 0):
        turn_right
    set while_condition to 1
    # End of the rotation on itself
    if ((R.see() does not return anything) and total_counter has the same length of token_array):
        print("My work here is done!!")
		exit()
    elif dist is less than d_th: 
		print("Found it!")
		R.grab() # if we are close to the token, we grab it.
		# FIRST ITERATION ONLY:
		global radius
		if instance is 0:
			first_iteration()
			set instance to 1
        else:
            dist, rot_y = find_that_token(first element of token_array)
            define threshold
			    while(dist is greater than threshold):
				    drive
				    dist, rot_y = find_that_token(first element of token_array)
                                    if rot_y is in between -a_th and a_th: # if the robot is well aligned with the token, we go forward
                                        print("Ah, here we are!.")
		                        drive
                                    elif rot_y is less than -a_th: # if the robot is not well aligned with the token, we move it on the left or on the right
		                        print("Left a bit...")
		                        turn_left
	                            elif rot_y is greater than a_th:
		                        print("Right a bit...")
		                        turn_right
        if(R.release() returns something):
            R.release()
            total_counter = total_counter + 1
	    drive_backwards
	    if(second_iteration is equal to 1):
            turn_left
		    while((R.see() does not return anything) and total_counter is different from the length of token_array):
                turn_right
        if(second_iteration is equal to 0):
		    start_time = take current time
		    while(R.see() returns something and second_iteration is equal to 0):
			    turn_right
			    set end_time to the current time
			    turn_right
			    set avg to end_time-start_time-0.3
			    # This is the time spent in the while loop - a thrashold
			    # This is done cause we have to not consider the check in the while but just the turning
			    # Even if we assume a time = 0 to check the condition of the while loop, the time calculated
			    # is given for going further (in fact we have to come back to see the marker again)
			    set second_iteration to 1
	    dist, rot_y = find_token()
    elif rot_y is in between -a_th and a_th: # if the robot is well aligned with the token, we go forward
        print("Ah, here we are!.")
	drive
    elif rot_y is less than -a_th: # if the robot is not well aligned with the token, we move it on the left or on the right
	print("Left a bit...")
	turn_left
    elif rot_y is greater than a_th:
	print("Right a bit...")
	turn_right
```
