# scape-generator
 A script to auto-generate save files (.scape files) for the game Townscaper. Still new to Python, so code might be a bit messy.


# How to use

You need Python to run this script (obviously). 
Put the whole folder at a location of your desire.
Then you can change the .ini. Put in the path to your save files (the one that's already there should work, just have to change the username, but please check).
Apart from that, you can change the mapsize there, as well as the filename.

!! Note that the filename ALWAYS has to be a .scape file, otherwise the game won't recognize/open it!!

The script does not give any feedback, but should finish pretty much instantaneously. You can double-check the save files folder ofc.

# Generating the file

This script saves data of the already generated objects during runtime.
When creating new objects, it then checks for already existing objects around it and adjusts the height of the new object.
