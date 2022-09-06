# Software Engineering Skills Test
## Matthew Cheng

### How to Run
All of my code can be found in the file parse.py, which takes one command line argument. It can be run like so:

python path/to/parse.py path/to/Programming-Assignment-Data

Ensure that the command line argument is the path to the directory which contains all of the xml and png files. In addition, it is important to note that since it is written in python, no compiling is required to run the program.

### Libraries
My program relies on the built-in python libraries: xml, sys, os, and array. I also use the png library, which has been included in the repository.

### My Solution
I decided to code my solution in python, as I have experience working with the png python library from a previous project. There are also many helpful built-in libraries that I was familiar with, which made it easier to reach a solution.

My approach to solving this problem was to find all of the bounding coordinates for the leaf nodes and to use those coordinates to draw yellow boxes. I did this by generating trees by parsing the xml files. Any of the leaf nodes of the trees had a length of 0, so I used recursion to add the 'bounds' attribute of each leaf node to a list. I then read in each of the png files and altered their pixel arrays using the coordinates from the list of bounding coordinates. Lastly, I output the new pixel arrays to png files that were then saved in the repository.

I decided to use an incremental approach when parsing files and drawing boxes, as not only did this seem like the easiest approach, but it was also the most space-efficient, as we would be reassigning variables for each file and box. Additionally, since I wanted the boxes to be more visible, I created ten more bounding boxes (lines 29-39) for each leaf node bounding box. I created these extra boxes at this step instead of during pixel assignment (lines 49-103) because I believe it would be more difficult to replicate at this stage. In a flat array, there is no simple way of creating an 11-pixel thick box for each coordinate in one step. This way, we also avoid repeating the value reassignment of many pixels, as there would be much overlap during this phase if we reassigned all surrounding pixels at once. It may have been easier to do this with a 2-dimensional array, however, if I did not make the array flat, then the contents of the array were replaced by a generator object that I could not easily figure out. For my last design decision, I choose to traverse the element tree containing the xml metadata using depth-first instead of breadth-first, as in general, depth-first is considered to be faster and I personally felt that it was easier to implement in this situation.
