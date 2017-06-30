This directory discribes how the process of finding the most efficient signal time for the 
traffic lights of Bengaluru.

Some definations: 

Interval: These are some time intervals. There are two types of intervals - change interval 
and clearance interval. Change interval is also called the yellow time which indicates 
the interval between the green and red signal indications for an approach. 
Clearance interval is also called all red and is provided after each yellow interval 
indicating a period during which all signal faces show red and is used for clearing 
off the vehicles in the intersection.

Green Interval: The time for which the green light is on.

Red Interval: The time for which the red light is on.

Phase:  A phase is the green interval plus the change and clearance intervals that follow it. 
Thus, during green interval, non conflicting movements are assigned into each phase. 
It allows a set of movements to flow and safely halt the flow before the phase of another 
set of movements start.

A device is placed on each of the four roads of the junction and each of the four roads 
can be devided into two types, from where the vehicles enter and from where they exit.


What the devices do:

The devices are capable of detecting live bluetooth devices in their vicinity.

They collect bluetooth information before every phase and then send this information 
to the server which now finds the signal time.

The server then responds with the signal time and sends it to the devices which then know 
when to sense and when to send the information for the next phase.

The sensing majorly occurs in the red intervals of the roads except for one of the lanes which is the 
one which is green in the present phase.

What the server does:

In short the server recieves the information from  the devices and calculates the most efficient
time. The calculation of the most efficient time is done using the BP algorithm discussed in this paper-
https://arxiv.org/abs/1401.3357v2

The BP algorithm is used and its comparison with the optimal BP* algorithm is done in the paper itself.

Overall the whole process if of  O(1) order and hence does not require direct information of the other 
junctions in the network.
