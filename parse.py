import xml.etree.ElementTree as ET
import sys
import os
import png
import array

def parseXML(file):
    # create element tree object
    tree = ET.parse(file)

    # get root element
    root = tree.getroot()

    return tree

def createImage(file, boxes):
    # from the boxes metadata, we reorganize the list of strings into a list of a list of ints
    # each list of ints represents the four bounding coordinates [lower x, lower y, upper x, upper y]
    for box in range(len(boxes)):
        boxes[box] = list(map(int, boxes[box][1:-1].replace(']',"").replace('[',",").split(',')))

    # temporary list to hold additional box layers
    outers = []

    # base offset for generating extra layers
    diff = [-1, -1, 1, 1]

    # for easier viewing, we generate extra layers to make the yellow boxes thicker
    for box in boxes:
        outers.append([max(sum(i), 0) for i in zip(box, diff)])
        outers.append([max(sum(i), 0) for i in zip(box, list(map(lambda x: x*-1, diff)))])
        outers.append([max(sum(i), 0) for i in zip(box, list(map(lambda x: x*2, diff)))])
        outers.append([max(sum(i), 0) for i in zip(box, list(map(lambda x: x*-2, diff)))])
        outers.append([max(sum(i), 0) for i in zip(box, list(map(lambda x: x*3, diff)))])
        outers.append([max(sum(i), 0) for i in zip(box, list(map(lambda x: x*-3, diff)))])
        outers.append([max(sum(i), 0) for i in zip(box, list(map(lambda x: x*4, diff)))])
        outers.append([max(sum(i), 0) for i in zip(box, list(map(lambda x: x*-4, diff)))])
        outers.append([max(sum(i), 0) for i in zip(box, list(map(lambda x: x*5, diff)))])
        outers.append([max(sum(i), 0) for i in zip(box, list(map(lambda x: x*-5, diff)))])

    # now we combine both lists of boxes together
    boxes = boxes + outers

    # read in the pixels and metadata from the png file
    r = png.Reader(sys.argv[1] + '/' + file + '.png')
    w, h, pixels, data = r.read_flat()

    # for each set of box coordinates
    for box in boxes:

        # we generate the horizontal box lines
        for x in range(box[0],box[2]+1):

            # we calculate the byte width, as it depends on whether alpha is true
            byte_width = 4 if data['alpha'] else 3

            # since the array is flat, we calculate the index of the desired pixel
            pos = x + box[1] * w

            # we set the new pixel value depending on if alpha is true
            new_val = (255, 215, 0, 255) if data['alpha'] else (255, 215, 0)

            # we replace the old byte array with a new one
            pixels[pos * byte_width : (pos+1) * byte_width] = array.array('B', new_val)

            # we calculate the byte width, as it depends on whether alpha is true
            byte_width = 4 if data['alpha'] else 3

            # since the array is flat, we calculate the index of the desired pixel
            pos = x + box[3] * w

            # we set the new pixel value depending on if alpha is true
            new_val = (255, 215, 0, 255) if data['alpha'] else (255, 215, 0)

            # we replace the old byte array with a new one
            pixels[pos * byte_width : (pos+1) * byte_width] = array.array('B', new_val)

        # and then the vertical box lines
        for y in range(box[1]+1, box[3]):

            # we calculate the byte width, as it depends on whether alpha is true
            byte_width = 4 if data['alpha'] else 3

            # since the array is flat, we calculate the index of the desired pixel
            pos = box[0] + y * w

            # we set the new pixel value depending on if alpha is true
            new_val = (255, 215, 0, 255) if data['alpha'] else (255, 215, 0)

            # we replace the old byte array with a new one
            pixels[pos * byte_width : (pos+1) * byte_width] = array.array('B', new_val)

            # we calculate the byte width, as it depends on whether alpha is true
            byte_width = 4 if data['alpha'] else 3

            # since the array is flat, we calculate the index of the desired pixel
            pos = box[2] + y * w

            # we set the new pixel value depending on if alpha is true
            new_val = (255, 215, 0, 255) if data['alpha'] else (255, 215, 0)

            # we replace the old byte array with a new one
            pixels[pos * byte_width : (pos+1) * byte_width] = array.array('B', new_val)

    # we create a new png file or overwrite an existing one
    annotated = open(file + '-annotated.png', 'wb')

    # we create a writer object with the previous dimensions and metadata
    writer = png.Writer(w, h, **data)

    # we write the pixels to the new file
    writer.write_array(annotated, pixels)

    annotated.close()

def annotate(file):
    # we generate an element tree of the nodes from the xml file
    tree = parseXML(sys.argv[1] + '/' + file)

    # this will be used to store the bounds of the yellow boxes that we will draw
    yellow_box_bounds = []

    # we grab the root of the element tree
    root = tree.getroot()

    # now by recursively iterating over the element tree, we add the bounds of leaf nodes to
    # our yellow_box_bounds list
    iterate(root, yellow_box_bounds)

    # using the list of bounds, we create a new image
    createImage(file[:-4], yellow_box_bounds)

def iterate(node, boxes):
    # if there is at least one child, then the node is not a leaf node
    if len(node) > 0:
        # we iterate through each child and call iterate again
        for child in node:
            iterate(child, boxes)
    # since there are no children, we must be at a leaf node, so we now add the
    # bounds of the node to the list
    else:
        boxes.append(node.attrib['bounds'])

if __name__ == '__main__':

    # using the user's command line argument as the path to the directory,
    # we get a list of all files within the directory
    files = os.listdir(sys.argv[1])

    # we now loop through the files, and if any files end in .xml,
    # we annotate their png files accordingly
    for file in files:
        if file[-3:] == "xml":
            annotate(file)
