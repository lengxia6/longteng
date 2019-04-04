# 第二天
##  递归
在函数内部，可以调用其他函数。如果一个函数在内部调用自身本身，这个函数就是递归函数。
阶乘： n的阶乘为n * (n-1) *  (n-2) * ... * 1

````
def factorial(n):
    if n == 1:
        return 1
    else:
        return n * factorial(n-1)

if __name__ == "__main__":
    print(factorial(5))
````

使用递归函数的优点是逻辑简单清晰，缺点是过深的调用会导致栈溢出。
````
def test():
    return test()
if __name__ == "__main__":
    test()
````
RecursionError: maximum recursion depth exceeded 递归异常，超过最大递归深度

x的n次幂 等于x 的n-1次幂乘x，x的0次幂等于1
````
def power(x, n):
    if n == 0:
        return 1
    else:
        return x * power(x, n -1)
if __name__ == "__main__":
    print(power(2, 6))
````

练习：取出n层嵌套列表里的所有元素
提示判断一个元素i是否是list 使用isinstance(i,list)函数

## 闭包
````
def npower():
    n = 2
    def  power(x):
        return x ** n
    return power

if __name__ == "__main__":
    f = npower()
    print(f(2))
    print(f(3))
````

在Python中创建一个闭包可以归结为以下三点
+ 闭包函数必须有内嵌函数
+ 内嵌函数需要引用该嵌套函数上一级命名空间中的变量
+ 闭包函数必须返回内嵌函数
在Python中，函数对象有一个__closure__属性，我们可以通过这个属性看看闭包的一些细节
````
def npower():
    n = 2
    def  power(x):
        return x ** n
    return power

if __name__ == "__main__":
    f = npower()
    print(f(2))
    print(f.__closure__)
    print(f.__closure__[0].cell_contents)
````
从这里可以看到闭包的原理，当内嵌函数引用了包含它的函数（enclosing function）中的变量后，
这些变量会被保存在闭包函数的__closure__属性中，成为闭包函数本身的一部分；
也就是说，这些变量的生命周期会和闭包函数一样。

## 装饰器


装饰器是可调用的对象，其参数是另一个函数（被装饰的函数），装饰器可以处理被装饰的函数，然后把它返回，
也可以将其替换成另一个函数或可调用对象

替换为另一个函数
````
def deco(func):
    def inner():
        print("running inner()")
    return inner

@deco
def target():
    print('running target()')


if __name__ == "__main__":
    target()

````
等效
````
def deco(func):
    def inner():
        print("running inner()")
    return inner


def target():
    print('running target()')


if __name__ == "__main__":
    target = deco(target)
    target()

````


它可以让被装饰的函数在不需要做任何代码变动的前提下增加额外的功能，
被装饰的函数当作参数传入，装饰器返回经过修饰后函数的名字；
内层函数（闭包）负责修饰被修饰函数。从上面这段描述中我们需要记住装饰器的几点属性，以便后面能更好的理解

+ 实质： 是一个函数
+ 参数：被装饰函数名
+ 返回：返回一个函数（被装饰的函数或者另一个函数）
+ 作用：为已经存在的对象添加额外的功能

统计函数的执行时间
````
import time

def decorator(func):
    def wrapper():
        start_time = time.time()
        func()
        end_time = time.time()
        print(end_time - start_time)

    return wrapper

@decorator
def func():
    print("hello world")
    time.sleep(1)

func()
````

返回函数被装饰的函数
````
def add_decorator(f):
    print("加法")
    return f

@add_decorator
def add_method(x, y):
    return x + y


print(add_method(2,3))

````

调用被装饰函数时,参数传递给返回的函数，所以wrap的参数要与被装饰函数一致，或者写成wrap(*arg, **dict)
````
def add_decorator(f):
    def wrap(x,y):
        print("加法")
        return f(x,y)
    return wrap

@add_decorator
def add_method(x, y):
    return x + y


print(add_method(2,3))
````

带参数的装饰器，本质是一个返回装饰器的函数
````
def out_f(arg):
    print("out_f" + arg)
    def decorator(func):
        def inner():
            func()
        return inner
    return decorator

@out_f("123")
def func():
    print("hello word")


func()
````
参数123传给函数out_f  返回装饰器decorator，@out_f("123")  就是@decorator

### 可迭代的对象，迭代器
迭代的意思是重复做一些事很多次，for循环就是一种迭代，列表，字典，元组都是可迭代对象
实现__iter__方法的对象都是可迭代的对象。 __iter__ 返回一个迭代器，所谓迭代器就是具有next方法的对象
在掉用next方法的时，迭代器会返回它的下一个值，如果没有值了，则返回StopIteration
````
>>> l = [1,2,3]   # l为可迭代对象
>>> b = l.__iter__()    #b 为迭代器
>>> next(b)
1
>>> next(b)
2
>>> next(b)
3
>>> next(b)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration
````
使用类定义迭代器，斐波那契数

````
class Fibs:
    def __init__(self):
        self.a = 0
        self.b = 1

    def __next__(self):
        self.a, self.b = self.b, self.a + self.b
        return self.a

    def __iter__(self):
        return self


fibs =Fibs()

for f in fibs:
    if f > 1000:
        print(f)
        break
````

### 生成器
1. 生成器函数
生成器是一种用函数语法定义的迭代器; 调用生成器函数返回一个迭代器
yield语句挂起生成器函数并向调用者发送一个值，迭代器的_next__继续运行函数

````
L = [[1, 2],[3, 4],[5,]]
def flat(L):
    for sublist in L:
        for e in sublist:
            yield e

for num in flat(L):
    print(num)
````

生成器send方法

````
def gen():
    for i in range(10):
        x = (yield i)
        print(x)

g = gen()
next(g)
print(g.send(11))
print(g.send(22))
````
生成器函数执行到yield 时就会暂停，执行send收继续运行到下一次循环yield时再暂停，send的值付给x

2. 生成器表达式
````
>>> f = ( x ** 2 for x in range(4))
>>> next(f)
0
>>> next(f)
1
>>> next(f)
4
>>> next(f)
9
````


### os 和os.path

os 模块
1.  返回当前目录
`os.getcwd()`
2.  列出目录的内容
` os.listdir()`
3. 创建目录
`os.mkdir("te")`
4.  删除空目录
`os.rmdir("te")`
5. 重命名
`os.rename('1.py','2.py')`
6.  删除文件
`os.remove('2.py')`
7. 执行系统命令
`os.system("dir")`
8. 退出程序
`os._exit(0)`
9. 遍历目录中的所有文件
`os.walk` 返回一个3元组生成器
当前目录的名称，当前目录中子目录的列表，当前目录中文件的列表
````
import os

g = os.walk("d:/py/peixun/python-dev")
print(next(g))
print(next(g))
````


os.path 模块
1. abspath()  将相对路径转化为绝对路径
`os.path.abspath(path)`
2. dirname()  获取完整路径当中的目录部分
`os.path.dirname("d:/1/test")`
3. basename()获取完整路径当中的主体部分
`os.path.basename("d:/1/test")`
4. split() 将一个完整的路径切割成目录部分和主体部分
`os.path.split("d:/1/test")`
5. join() 将2个路径合并成一个
`os.path.join("d:/1", "test")`
6. getsize()  获取文件的大小
`os.path.getsize(path)`
7. isfile() 检测是否是文件
`os.path.isfile(path)`
8. isdir()  检测是否是文件夹
`os.path.isdir(path)`

列出目录下包括子目录的所有文件
````
import os

for dirpath, dirames, filenames  in os.walk("d:/py/peixun/python-dev"):
    print('[' + dirpath + ']')
    for filename in filenames:
        print(os.path.join(dirpath, filename))
````

### 练习
* 递归函数列出所有文件 使用os.listdir os.isfile
* 练习找出单个目录中的最大文件
* 练习找出目录树中的最大文件


###  作业
复制目录数,拷贝目录a到a.bak