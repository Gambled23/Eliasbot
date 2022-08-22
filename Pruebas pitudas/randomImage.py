import os
import random 

path="pictures\elias"
files=os.listdir(path)
d=random.choice(files)
print(d)