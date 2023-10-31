# ResearchTrack1 - Assignment 1
## The objective of the asssignment
The request is to program the robot to put the markers present in the arena near to each other, performing it with the minimum possible movements done by the robot.
## The assuptions
The ony assumption I made to write the program is that all markers are placed in a circle in the arena. I do not know the initial position of the robot nor the absolute position of the marker.
## The first step
To make the robot move as little as possible, I had to identify the centre of the arena. To do that I use the only assumption that I have made.
The first step is scanning with a rotation on the starting position every marker I have near the robot. Then I procede to go to the nearest marker, and do a second rotation. Doing this I save all the ids of the markers in a vector, saving the distances as well. The marker with the longest distance from the robot is the one that I choose as target. The line starting where I am linking to the position of the marker is going through the centre of the arena.
To calculate the radius I subtract to the distance from the further marker with the one I have taken (that is the minimun distance) and dividing this by 2.
The I drive forward until I have driven one radius length and I stop, realising the marker. This will be the target I will take as reference for all the other markers I will bring to the centre for now on, and it will be remembered beacause I move its id position in the array in the 0 spot.
