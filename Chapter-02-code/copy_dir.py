import os, sys
maxfileload = 1000000
blksize = 1024 * 50

def copyfile(pathFrom, pathTo, maxfileload=maxfileload):
    """
    将文件逐字节从pathFrom复制到pathTo，使用二进制模式读写
    """

    if os.path.getsize(pathFrom) <= maxfileload:
        bytesFrom = open(pathFrom, 'rb').read()
        open(pathTo, 'wb').write(bytesFrom)
    else:
        fileFrom = open(pathFrom, 'rb')
        fileTo = open(pathTo, 'wb')
        while True:
            bytesFrom = fileFrom.read(blksize)
            if not bytesFrom:
                break
            fileTo.write(bytesFrom)

def copytree(dirFrom, dirTo, verbose=0):
    """
    拷贝目录
    """
    fcount = dcount = 0
    for filename in os.listdir(dirFrom):
        pathFrom = os.path.join(dirFrom, filename)
        pathTo = os.path.join(dirTo, filename)
        if not os.path.isdir(pathFrom):
            try:
                if verbose > 1:
                    print("拷贝", pathFrom, "到", pathTo)
                copyfile(pathFrom, pathTo)
                fcount += 1
            except:
                print("拷贝错误", pathFrom, "到", pathTo)
        else:
            if verbose:
                print('copying dir', pathFrom, 'to', pathTo)
            try:
                os.mkdir(pathTo)  #创建子目录
                below = copytree(pathFrom, pathTo, verbose) # 递归
                fcount += below[0]
                dcount += below[1]
                dcount += 1
            except:
                print("创建错误", pathFrom, "到", pathTo)
                print(sys.exc_info()[0], sys.exc_info()[1])
    return fcount, dcount

if __name__ == "__main__":
    dirForm = r"d:\BaiduYunDownload"
    dirTo = r"d:\BaiduYunDownload.bak"
    os.mkdir(dirTo)
    fcount, dcount = copytree(dirForm, dirTo, verbose=2)
    print("拷贝目录: %d;拷贝文件: %d" %  (fcount, dcount))



