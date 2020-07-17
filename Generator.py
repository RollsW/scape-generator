import xml.etree.cElementTree as et
import random
from configparser import ConfigParser
import os
import statistics

# Reading in .ini data, as well as creating dict for saving heights at coordinates.
config = ConfigParser()
config.read("settings.ini")
cwd = os.getcwd()
gameDir = config.get("gamepath", "GAME_PATH")
fileName = config.get("filename", "FILE_NAME")
coordinates = dict()

# Added padding because the underlying grid is not random - we see particular features coming back
# unless we drop the town at a random point on the wider grid
x_padding = random.randrange(-1000, 1000)
y_padding = random.randrange(-1000, 1000)

minX = x_padding
maxX = x_padding + int(config.get("mapsize", "X_dimension"))
minY = y_padding
maxY = y_padding + int(config.get("mapsize", "Y_dimension"))

# minX = int(minX)
# maxX = int(maxX)
# minY = int(minY)
# maxY = int(maxY)


cMinX = minX - (minX % 9)
cMaxX = maxX - (maxX % 9)
cMinY = minY - (minY % 9)
cMaxY = maxY - (maxY % 9)
# Standard height list, as well as weights for normal list and generated list based on surroundings.
heightList = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
weights = [4, 10, 4, 2, 1, 0.5, 0.3, 0.07, 0.05, 0.03, 0.03]
adaptedWeights = [0.25, 0.25, 0.4, 0.05, 0.05]

# Add a new corner to output file
def addCorner(x, y, ct):
    corner = et.SubElement(corners, "C")
    cX = et.SubElement(corner, "x")
    cY = et.SubElement(corner, "y")
    count = et.SubElement(corner, "count")
    cX.text = str(x)
    cY.text = str(y)
    count.text = str(ct)


# Add a new voxel to output file
def addVoxel(col, ht):
    voxel = et.SubElement(voxels, "V")
    t = et.SubElement(voxel, "t")
    h = et.SubElement(voxel, "h")
    t.text = str(col)
    h.text = str(ht)


# Get the median of surrounding files, based on input coordinates.
def getNearbyMedian(vec):
    heights = []
    for x in range(vec[0] - 9, vec[0] + 10, 9):
        for y in range(vec[1] - 9, vec[1] + 10, 9):
            if x != y:
                if (x, y) in coordinates:
                    heights.append(coordinates.get((x, y)))
    if not heights:
        return 0
    else:
        return int(round(statistics.median(heights)))


# Get an adapted height list, based on the input height.
def getHeights(ht):
    if ht > 2:
        return [ht - 2, ht - 1, ht, ht + 1, ht + 2]
    else:
        return [0, 1, 2, 3, 4]


# Adding basic data to XML, eg cam positioning.
root = et.Element("SaveData")
root.set("xmlns:xsd", "http://www.w3.org/2001/XMLSchema")
root.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")

saveString = et.SubElement(root, "saveString")

cam = et.SubElement(root, "cam")
camX = et.SubElement(cam, "x")
camY = et.SubElement(cam, "y")
camZ = et.SubElement(cam, "z")
camX.text = "132"
camY.text = "178"
camZ.text = "203"

corners = et.SubElement(root, "corners")
voxels = et.SubElement(root, "voxels")
# Nested loop to cover each viable x/y coordinate.
for x in range(cMinX, cMaxX, 9):
    for y in range(cMinY, cMaxY, 9):
        med = getNearbyMedian([x, y])
        if (
            med > 0
        ):  # Choose if there actually is a relevant median, if yes create adapted height list and use that for weighted random height.
            randCount = random.choices(getHeights(med), adaptedWeights)
        else:
            # Choose weighted random height based on the standard list.
            randCount = random.choices(heightList, weights, k=1)
        addCorner(x, y, randCount[0])
        current = (x, y)
        # Save the created coordinate/height pair in dict
        coordinates[current] = randCount[0]
        if randCount[0] > 0:
            # Add the needed voxels for the currently created corner.
            for i in range(randCount[0]):
                if i == 0:
                    addVoxel(15, 0)
                else:
                    addVoxel(random.randrange(14), i)
smallJPG = et.SubElement(root, "smalljpg")
bigjpg = et.SubElement(root, "bigjpg")

# Wrap up data, create file.
tree = et.ElementTree(root)
os.chdir(gameDir)
tree.write(fileName)
os.chdir(cwd)
