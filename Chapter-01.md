# 第一天
## 一、git
#### 1. 版本控制
什么是版本控制？我为什么要关心它呢？版本控制是一种记录一个或若干文件内容变化，以便将来查阅特定版本修订情况的系统。
在本书所展示的例子中，我们仅对保存着软件源代码的文本文件作版本控制管理，但实际上，你可以对任何类型的文件进行版本控制。

版本控制解决的问题，许多人习惯用复制整个项目目录的方式来保存不同的版本，或许还会改名加上备份时间以示区别。
这么做唯一的好处就是简单。不过坏处也不少：有时候会混淆所在的工作目录，一旦弄错文件丢了数据就没法撤销恢复。

常见版本控制系统，git，svn，vcs

什么是git? linux开源社区， Linus Torvalds为linux内核项目，开发的一个分布式版本控制系统
* 速度
* 简单
* 支持大量并行开发分支
* 完全分布式
* 支持超大规模的项目，如linux内核项目
#### 2. 安装git
windows 安装git
````
https://git-scm.com/
````
点击download下载，下一步，下一步即可

#### 3. 创建git项目
两种创建git项目的方法
* git init
* git clone

**对现有项目，开始使用git，打开git bash进入项目目录**
````
git init
````
初始化后，在当前目录下会出现一个名为 .git 的目录，所有 Git 需要的数据和资源都存放在这个目录中。
如果当前目录下有几个文件想要纳入版本控制，需要先用 git add 命令告诉 Git 开始对这些文件进行跟踪，然后提交
````
git add hw.py
git commit -m 'init this project'
````
* git add 对文件进行跟踪，添加到暂存区
* git commit 提交到本地仓库
**从现有项目克隆**
如果想从现有项目复制，就需要用到git clone
````
git clone https://github.com/jiam/python-dev.git
````
当前目录就会出现python-dev这个项目

#### 4. 将本地的git项目push到远程仓库如：github
* 在github注册账号
* 登陆github
* 创建一个github项目与本地项目同名
````
echo "# test" >> README.md
git init
git add README.md
git commit -m "first commit"
git remote add origin https://github.com/jiam/test.git
git push -u origin master
````
* git remote add  添加远程仓库
* git push 将本地仓库推送到远程仓库

#### 5. git的回滚
* 工作区
* 暂存区
* 已提交区

工作区即当前目录，使用git add 命令后，文件被追踪，状态为在暂存；git commit后提交到仓库
**只修改文件为执行git add**
````
git checkout filename
````
**修改文件后，执行git add 但未执行git commit**
````
git reset HEAD
git checkout filename
````
**修改文件后，执行了git add和git commit**
````
git reset --hard HEAD^
````

#### 6. 添加分支
在仓库中添加一个新的分支
````
git branch dev
````
将新的分支push到远程仓库
````
git push --set-upstream origin dev
````
#### 7. 合并分支
在dev中更改代码后想合并回master
````
git checkout master
git merge dev
````
#### 8. 配置git密码
````
.git/config

[credential]
    helper = store
````

## 二、 pycharm中使用git
#### 1. 新建git项目
打开pycharm->vcs->checkout from versin control->git 
填写git的url，和本地的项目目录

#### 2. git add
右键->git->add

#### 3. git commit
右键->git->commit

#### 4. 未提交回滚
右键->git->revert

#### 5. 已提交回滚
右键->git->Repository->Rest HEAD
#### 6. 增加分支
右键->git->Repository->Branches->New Branch 填入分支名称

#### 7. 切换分支
右键->git->Repository->Branches->分支名->checkout

#### 8. 合并分支
右键->git->Repository->Merge Changes->选择要合并的分支

#### 9. 推送到远程
右键->git->Repository->push

## 三、 回顾python基础
编写一个通讯录程序，实现增删改查功能
#### 1.设计数据结构
一条记录： 姓名，电话， id
一个通讯录：列表，里面元素为记录

#### 2. 函数设计
* 增加 add_record
* 查询 query_record
* 修改 change_record
* 删除 delete_record

#### 3. 菜单设计
* main函数
* while 循环
* 选择相应功能
示例
````

        通讯录
        1. 添加
        2. 查找
        3. 删除
        4. 修改
        5. 退出
        
请选择操作:1
请输入姓名:jia
请输入电话:123
添加成功

        通讯录
        1. 添加
        2. 查找
        3. 删除
        4. 修改
        5. 退出
        
请选择操作:
````


## 四、使用面向对象实现该通讯录
#### 1.设计数据结构
* 记录类 Record
* 通讯录类 PhoneBook

#### 2. 类方法设计
* Record __init__、 set_number
* PhoneBook __init__、add_record、query_record、change_record、delete_record
#### 3. 菜单设计不变

## 五、 python对象序列化pickle
pickle模块是一种的对象序列化工具；对于内存中几乎任何的python对象，都能把对象转化为字节串，
这个字节串可以随后用来在内存中重建最初的对象。pickle模块能够处理我们用的任何对象，列表，字典
嵌套组合以及类和实例

#### 1. dumps和 loads
列表对象
````
>>> import pickle
>>> l = [1,2,3]
>>> pickle.dumps(l)
b'\x80\x03]q\x00(K\x01K\x02K\x03e.'
>>> b = pickle.dumps(l)
>>> b
b'\x80\x03]q\x00(K\x01K\x02K\x03e.'
>>> pickle.loads(b)
````

字典对象
````
>>> d = {"id":1, "name": "贾敏强", "phone_number":"15801396646"}
>>> pickle.dumps(d)
b'\x80\x03}q\x00(X\x02\x00\x00\x00idq\x01K\x01X\x04\x00\x00\x00nameq\x02X\t\x00\x00\x00\xe8\xb4\xbe\xe6\x95\x8f\xe5\xbc\xbaq\x03X\x0c\x00\x00\x00phone_numberq\x04X\x0b\x00\x00\x0015801396646q\x05u.'
>>> b = pickle.dumps(d)
>>> pickle.loads(b)
{'id': 1, 'name': '贾敏强', 'phone_number': '15801396646'}
````

类和实例
````
import pickle


class Record:
    def __init__(self, name, phone_number):
        self.name = name
        self.phone_number = phone_number


R = pickle.dumps(Record)
print(R)
print(pickle.loads(R))

record = Record("贾敏强", "15801396646")
r = pickle.dumps(record)
print(r)
print(pickle.loads(r))
````

#### 2. dump 和load
````
import pickle

L = [1, 2, 3]
with open("d://L.dat", "wb") as f:
    pickle.dump(L, f)
with open("d://L.dat", "rb") as f:
    print(pickle.load(f))


class Record:
    def __init__(self, name, phone_number):
        self.name = name
        self.phone_number = phone_number


with open("d:/Record.dat", "wb") as f:
    pickle.dump(Record, f)
with open("d:/Record.dat", "rb") as f:
    print(pickle.load(f))

record = Record("贾敏强", "15801396646")
with open("d:/record.dat", "wb") as f:
    pickle.dump(record, f)
with open("d:/record.dat", "rb") as f:
    print(pickle.load(f))


records = []
records.append(record)
with open("d:/records.dat", "wb") as f:
    pickle.dump(records, f)

with open("d:/records.dat", "rb") as f:
    print(pickle.load(f))

````

## 六、 练习
#### 1. 使用json将通讯录（函数）序列化
#### 2. 使用pickle将通讯录（面向对象）序列化











