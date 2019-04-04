# 第15天 vue+django 前后端分离

## 安装node
下载地址[node](https://nodejs.org/dist/v10.15.1/node-v10.15.1-x64.msi)

配置npm
```
npm config set registry https://registry.npm.taobao.org

npm config set sass_binary_site https://npm.taobao.org/mirrors/node-sass/

```
## 前后段分离
1. 前端一个项目，后端一个项目
2. 可以自由的选择框架和语言(javascript/typescripts),(css,html,js) vue,react angularjs mvvm, python(django,flask) java spring + springmvc + springboot + springbooot, php thinkphp zenphp...,golang ...
3. 专业的人干专业的事， 前端web开发师，后端服务开发工程师
4. 约定api规范，ajax + json  restful

## 接口规范
1. 登录接口
2. 新建项目接口  协议http   方法post  数据data {"name","dscrption"}
3. 编辑项目接口
4. 删除项目接口
5. 列出项目接口
6. 查找项目接口
7. 批量删除接口


## moke
1. 前端mock
2. 后端postman 测试

## 前端项目代码

讨论组下载

进入解压目录执行
`npm install`

运行开发服务器
`npm run dev`

## 创建后端项目

1. 项目名称

vue_django

2. app名称
app

3. 数据库名称
vue_django
运行migrate

4. 新建一个超级用户

5. 配置login 的url

6. 编写loing 的view 函数
