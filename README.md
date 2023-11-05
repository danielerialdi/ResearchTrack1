# ResearchTrack1 - Assignment 1
## The objective of the assignment
We have been given a simulator that is able to simulate a robot in a 2D environment and make it move around the arena and interact with the objects (markers) in it.
The robot is able to identify the markers in its field of view and identify the distance and the angle between the position of itself and the one of the object detected. 
The request is to program the robot to put the markers present in the arena near to each other, performing it with the minimum possible movements done by the robot.
## How to run the program
To be able to run the program it is necessary to pass to 'run.py' the filename of the script, while being in the right folder, as it follows:
```bash
$ python2 run.py assignment.py
```
## The assuptions
The ony assumption I made to write the program is that all markers are placed in a circle in the arena. 
I do not know the initial position of the robot nor the absolute position of the marker.
## Possible strategies
To be able to put all the markers near to each other, I could place all of them near to one take as reference; this would have meant to move all the markers except one (in this case 5) to an edge of the arena. This would have been easier to compute, but the robot would have spent more time moving around the arena. 
So the other possibility was to identify the centre of the arena and bring all the markers there; this requires an analisys prior to the beginning of the displacements of the markers, but the robot has to move as little as possible to reach the requirement of the assignment. 
## How the script works
The chosen alternative between the ones presented was the second one: bring all the markers in the centre of the arena.
### The first step
To identify the centre of the arena I use the only assumption that I have made.
The first step is scanning with a rotation of 360 degrees on the starting position every marker I have near the robot. Then I procede to go to the nearest marker, and do a second rotation. Doing this I save all the ids of the markers in an array, saving the distances as well. The marker with the longest distance from the robot is the one that I choose as target. The line starting where I am linking to the position of the marker is going through the centre of the arena.
To calculate the radius I subtract to the distance from the further marker with the one I have taken (that is the minimun distance) and dividing this by 2.
The I drive forward until I have driven one radius length and I stop, realising the marker. This will be the target I will take as reference for all the other markers I will bring to the centre for now on, and it will be remembered beacause I move its id position in the array in the 0 spot.
### The other markers
Once I have set the first token in the middle of the arena, I drive backwards a little to make sure to not hit the object just released and I make the robot turn until I do not see any token in the field of view. When this occurs, I can turn back for an instance to have in my visual range a token, that will be the one that I'll grab next. It is now possible to analize the distance and the angle of the marker with respect to the robot and now I can let the robot drive towards it.
The robot when arrives at the destination grabs the token, and while it does not see the reference marker (the one put in the middle) it turns. Then it will drive towards it and when it arrives at a certain trashold it will stop, releasing the maker. 
## Functions in the code
There are several functions used in the script code, some of them are from the libraries of the robot while some others were written to ease off some operations and to make the code more readable and understandable.
In the table that follow all the functions are grouped and explained:
| Function | The purpose |
| -------- | -------- |
| drive(speed, seconds) | Sets a linear velocity for the robot with the first parameter and with 'seconds' it imposes to keep that velocity for a certain amount of time. |
| turn(speed,seconds) | It is similar to the drive function, but sets an angular velocity, instead of a linear one. |
| update_token_array(m) | Appends the offset of a marker seen for the first time by the robot to the array 'token_array' that is an array devolved to this duty. It checks if the offset is not already present in the array and that 'm' is an object of type int; only if those conditions are satisfied, it will append the object to the array.|
| find_token() | Finds the closest token between the ones that the robot has in its range of view. Returns the distance and the angle from the closest token. If no token is detected returns -1 for both the distance and the angle. |
| find_that_token(m)| Checks all the token that the robot sees in its range of view. If it is present the token wanted, recognizable by the offset 'm' passed as an argument, it returns the distance and the angle. If the robot cannot se the token wanted, it turns on itself a little and repeats the operation. |
| min_dist() | Compares the distance between the markers in the robot's range of view and returns the smallest distance and the index of the corresponding marker. |
| max_dist() | Compares the distance between the markers in the robot's range of view and returns the biggest distance and the index of the corresponding marker. |
| diam_dist() | Computes the maximum distance between all tokens and returns it with the offset which correspond to it. The pseudocode follows to understand better how the function works. |
| first_iteration() | Computes the centre of the arena and guides the robot there. It does not return anything, it is only needed to make the code more readable. The pseudocode for this function is presented later. |

Pseudocode for diam_dist():
```
array_all_token = empty  
array_dist = empty  
global token_array
first = True  
temp = True  
markers = markers that the robot sees  
while (temp is True):  
    turn(10,0.3)  
    if (markers are different from the ones the root is seeing):  
        markers = markers that the robot sees  
        for (every markers m in the list of the ones the robot sees):  
            if((the offset of m is present in 'array_all_token') and (first is True)):  
                first = False  
                dist, index = min_dist()  
             if(the length of array_all_token is equal to the length of token_array):  
                 temp = False
             if(the offset of m is not present in 'array_all_token'):
                 append to array_all_token the offset of m
                 append to array_dist the distance of m
                 update_token_array(offset of m)
i = index of the maximum in array_dist
return (maximum in array_dist), array_all_token[i] 
```

Pseudocode for first_iteration():
```
global first_iteration_condition
while(first_iteration_condition is False):
    dist, indexD = diam_dist()  
    find_that_token(indexD)  
    markers = markers that the robot sees
    for (every markers m in the list of the ones the robot sees):
        update_token_array(m)
        if((distance of m) is between (dist - d_th) and (dist + d_th)):
            rot_y = angle of m
            while(rot_y is greater that -a_th):
                if(rot_y is less than -a_th):
                    turn(-2,0.5)
                elif(rot_y is greater than a_th):
                    turn(2,0.5)
                dist, rot_y = find_that_token(offset of m)
                if(rot_y is between -a_th and a_th):
                    first_iteration_condition = True
                    break
global token_array
dist_max = max_dist()
dist_min = min_dist()
diameter = dist_max[0]-dist_min[0]
for (every i in range 0, (length of token_array - 1)):
    if(token_array[i] is equal to dist_min[1]):
        pop i element in token_array
insert dist_min[1] in token_array in position 0
global radius
radius = diameter/2.0
param = diameter
while(param is greater than radius):
    param, rot_y = find_that_token(indexD)
    dist_min = min_dist()
    param = param-dist_min[0]
    drive(10,0.3)
```
