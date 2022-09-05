import xml.etree.ElementTree as ET
import sys
import os
import png, array
# python parse.py ../Programming-Assignment-Data

def parseXML(file):
    # create element tree object
    tree = ET.parse(file)

    # get root element
    root = tree.getroot()

    return tree

def createImage(file, boxes):
    # create image
    for box in range(len(boxes)):
        boxes[box] = list(map(int, boxes[box][1:-1].replace(']',"").replace('[',",").split(',')))

    outers = []
    diff = [-1, -1, 1, 1]
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

    boxes = boxes + outers

    r = png.Reader(sys.argv[1] + '/' + file + '.png')
    w, h, pixels, data = r.read_flat()

    for box in boxes:
        for x in range(box[0],box[2]+1):
            point = (x, box[1])
            byte_width = 4 if data['alpha'] else 3
            pos = point[0] + point[1] * w
            new_val = (255, 215, 0, 255) if data['alpha'] else (255, 215, 0)
            pixels[pos * byte_width : (pos+1) * byte_width] = array.array('B', new_val)

            point = (x, box[3])
            byte_width = 4 if data['alpha'] else 3
            pos = point[0] + point[1] * w
            new_val = (255, 215, 0, 255) if data['alpha'] else (255, 215, 0)
            pixels[pos * byte_width : (pos+1) * byte_width] = array.array('B', new_val)

        for y in range(box[1]+1, box[3]):

            point = (box[0], y)
            byte_width = 4 if data['alpha'] else 3
            pos = point[0] + point[1] * w
            new_val = (255, 215, 0, 255) if data['alpha'] else (255, 215, 0)
            pixels[pos * byte_width : (pos+1) * byte_width] = array.array('B', new_val)

            point = (box[2], y)
            byte_width = 4 if data['alpha'] else 3
            pos = point[0] + point[1] * w
            new_val = (255, 215, 0, 255) if data['alpha'] else (255, 215, 0)
            pixels[pos * byte_width : (pos+1) * byte_width] = array.array('B', new_val)

    annotated = open(sys.argv[1] + '/' + file + '-annotated.png', 'wb')
    writer = png.Writer(w, h, **data)
    writer.write_array(annotated, pixels)

def annotate(file):
    tree = parseXML(sys.argv[1] + '/' + file)

    yellow_box_bounds = []
    root = tree.getroot()

    iterate(root, yellow_box_bounds)

    createImage(file[:-4], yellow_box_bounds)

def iterate(node, boxes):
    if len(node) > 0:
        for child in node:
            iterate(child, boxes)
    else:
        boxes.append(node.attrib['bounds'])

if __name__ == '__main__':

    files = os.listdir(sys.argv[1])

    for file in files:
        if file[-3:] == "xml":
            annotate(file)
