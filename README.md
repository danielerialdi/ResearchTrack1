# ResearchTrack1 - Assignment 1
## The objective of the assignment
We have been given a simulator that is able to simulate a robot in a 2D environment and make it move around the arena and interact with the objects (markers) in it.
The robot is able to identify the markers in its field of view and identify the distance and the angle between the position of itself and the one of the object detected. 
The request is to program the robot to put the markers present in the arena near to each other, performing it with the minimum possible movements done by the robot.
## How to run the program
To be able to run the program it is necessary to pass to 'run.py' the filename of the script, while being in the right folder, as it follows:
```python
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
To make the robot move as little as possible, I had to identify the centre of the arena. To do that I use the only assumption that I have made.
The first step is scanning with a rotation on the starting position every marker I have near the robot. Then I procede to go to the nearest marker, and do a second rotation. Doing this I save all the ids of the markers in a vector, saving the distances as well. The marker with the longest distance from the robot is the one that I choose as target. The line starting where I am linking to the position of the marker is going through the centre of the arena.
To calculate the radius I subtract to the distance from the further marker with the one I have taken (that is the minimun distance) and dividing this by 2.
The I drive forward until I have driven one radius length and I stop, realising the marker. This will be the target I will take as reference for all the other markers I will bring to the centre for now on, and it will be remembered beacause I move its id position in the array in the 0 spot.

