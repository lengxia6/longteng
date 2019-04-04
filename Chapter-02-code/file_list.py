import os


def listfile(dir):
    for file in os.listdir(dir):
        path = os.path.join(dir, file)
        if not os.path.isdir(path):
            print(path)
        else:
            listfile(path)


dir = "d:/py/peixun/python-dev"
listfile(dir)