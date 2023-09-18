import os
import glob

for filename in glob.glob("output_images/*_o4.jpg"):
    os.remove(filename)

