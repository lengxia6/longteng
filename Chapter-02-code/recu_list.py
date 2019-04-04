"""
取出嵌套列表内的所有元素
"""


def recu_list(L):
    for i in L:
        if isinstance(i,list):
            recu_list(i)
        else:
            print(i)


if __name__ == "__main__":
    L = [1, 2, [4, 5], 3]
    recu_list(L)