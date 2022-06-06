import os
curpath=os.path.dirname(os.path.realpath(__file__))
path=os.path.join(curpath,"config.txt")
with open(path,encoding="utf-8") as fp:
    read=fp.read()
    print(read)

