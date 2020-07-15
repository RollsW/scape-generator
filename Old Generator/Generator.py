import xml.etree.cElementTree as et
import random
from configparser import ConfigParser
import os

config = ConfigParser()
config.read("settings.ini")
cwd = os.getcwd()
gameDir = config.get("gamepath", "GAME_PATH")
fileName = config.get("filename", "FILE_NAME")

minX = config.get("mapsize", "MIN_X")
maxX = config.get("mapsize", "MAX_X")
minY = config.get("mapsize", "MIN_Y")
maxY = config.get("mapsize", "MAX_Y")

minX = int(minX)
maxX = int(maxX)
minY = int(minY)
maxY = int(maxY)

cMinX = minX - (minX % 9)
cMaxX = maxX - (maxX % 9)
cMinY = minY - (minY % 9)
cMaxY = maxY - (maxY % 9)

heightList = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
weights = [4, 10, 4, 2, 1, 0.5, 0.3, 0.07, 0.05, 0.03, 0.03]


def addCorner(x, y, ct):
    corner = et.SubElement(corners, "C")
    cX = et.SubElement(corner, "x")
    cY = et.SubElement(corner, "y")
    count = et.SubElement(corner, "count")
    cX.text = str(x)
    cY.text = str(y)
    count.text = str(ct)


def addVoxel(col, ht):
    voxel = et.SubElement(voxels, "V")
    t = et.SubElement(voxel, "t")
    h = et.SubElement(voxel, "h")
    t.text = str(col)
    h.text = str(ht)


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

for x in range(cMinX, cMaxX, 9):
    for y in range(cMinY, cMaxY, 9):
        randCount = random.choices(heightList, weights, k=1)
        addCorner(x, y, randCount[0])
        if randCount[0] > 0:
            for i in range(randCount[0]):
                if i == 0:
                    addVoxel(15, 0)
                else:
                    addVoxel(random.randrange(14), i)
smallJPG = et.SubElement(root, "smalljpg")
bigjpg = et.SubElement(root, "bigjpg")


tree = et.ElementTree(root)
os.chdir(gameDir)
tree.write(fileName)
os.chdir(cwd)
