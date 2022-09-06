# Software Engineering Skills Test
## Matthew Cheng

### How to Run
All of my code can be found in the file parse.py, which takes one command line argument. It can be run like so:

python path/to/parse.py path/to/Programming-Assignment-Data

Ensure that the command line argument is the path to the directory which contains all of the xml and png files.

### Libraries
My program relies on the built-in python libraries: xml, sys, os, and array. I also use the png library, which has been included in the repository.

### My Solution
I decided to code my solution in python, as I have experience working with the png python library from a previous project. There are also many helpful built-in libraries that I was familiar with, which made it easier to reach a solution.

My approach to solving this problem was to find all of the bounding coordinates for the leaf nodes and to use those coordinates to draw yellow boxes. I did this by generating trees by parsing the xml files. Any of the leaf nodes of the trees had a length of 0, so I used recursion to add the 'bounds' attribute of each leaf node to a list. I then read in each of the png files and altered their pixel arrays using the coordinates from the list of bounding coordinates. Lastly, I output the new pixel arrays to png files that were then saved in the repository.
