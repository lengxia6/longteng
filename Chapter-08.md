#  第八天

##  Django介绍
Django是一个高级Python Web框架，鼓励快速开发和实用的设计。
由经验丰富的开发人员开发，它可以处理Web开发的大部分问题，
因此可以专注于编写应用程序，而无需重新发明轮子。

Django 特点
1.  快速: Django旨在帮助开发人员尽可能快地完成应用程序
2.  安全: Django严肃对待安全并帮助开发人员避免许多常见的安全错误
3.  可伸缩:  Django快速灵活扩展的能力
4.  丰富的组件: Django 内置各种web开发常用功能组件

## Django安装

使用pip
```
pip install django
```

验证django
```
>>> import django
>>> django.get_version()
'2.1.4'

```

## 创建一个项目

在pycharm Terminal中输入

`django-admin startproject mysite`

项目结构
```
└── mysite
    ├── manage.py
    └── mysite
        ├── __init__.py
        ├── settings.py
        ├── urls.py
        └── wsgi.py

```

+ 顶部mysite:  项目根目录。 它的名字与Django无关; 你可以将它重命名为任何你喜欢的名字
+ manager.py: 一个命令行实用程序，可让您以各种方式与此Django项目进行交互。
+ 内部mysite: 项目的实际Python包。 它的名字是你需要用来导入任何东西的Python包名
+ mysite/__init__.py: 一个空文件，告诉Python这个目录应该被视为一个Python包
+ mysite/settings.py:  这个Django项目的配置文件
+ mysite/urls.py:  这个Django项目的URL声明
+ mysite/wsgi.py:  WSGI兼容的Web服务器,为项目提供服务的入口点

以开发模式运行服务器

```
cd mysite
python manage.py runserver
```

访问django 
在浏览器打开http://127.0.0.1:8000

修改开发服务器默认端口
````
cd mysite
python manage.py runserver 8080
````

默认开发服务器监听127.0.0.1
修改监听ip
```
python manage.py runserver 0:8000
```

## 创建第一个app
项目和应用程序有什么区别？ 应用程序是一种Web应用程序，它可以执行某些操作，
例如博客系统，公共记录数据库或简单的民意调查应用程序。 
项目是特定网站的配置和应用程序的集合。 项目可以包含多个应用程序。

````
python manage.py startapp myapp
````

myapp目录结构

````
myapp
├── admin.py
├── apps.py
├── __init__.py
├── migrations
│   └── __init__.py
├── models.py
├── tests.py
└── views.py
````

+ admin.py  将models注册到djangoadmin
+ apps.py  app 配置
+ __init__.py  表明该文件夹为包
+ migrations  数据库版本升级
+ models.py 数据库管理
+ tests.py  测试文件
+ views  视图文件

编辑myapp/views.py
```
from django.http import HttpResponse

# Create your views here.


def index(request):
    return HttpResponse("Hello world,You're at myapp index")
```

创建myapp/urls.py

```
from django.urls import path

from .  import views


urlpatterns = [
    path('', views.index, name='index')
]

```
编辑mysite/urls.py

```
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls'))
]
```

注册应用

```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myapp.apps.MyappConfig',
]
```
注意：注意到INSTALLED_APPS已经有许多其他的应用了 (还有 MIDDLEWARE, 在settings的下面)。这些应用为  Django administration site 提供了支持和许多功能(包括会话，认证系统等)。
再次访问 http://127.0.0.1:8000/


开始一个新项目
+ 使用django的工具创建一个网站项目和应用
+ 创建模型（models）
+ 使用django的admin站点来填充网站数据
+ 创建视图函数（views）来取回相应的数据，并用模板（templates）渲染成HTML页面
+ 创建urlconf，将不同的url分发给特定的视图函数（views）
+ 添加用户认证和会话（sessions）
+ 表单
+ 编写单元测试

## 创建一个新的项目
创建一个图书管理项目，这个网站的目标是为一个小型的图书馆提供一个在线的目录。在这个小型图书管里，用户能浏览书籍和管理他们的账户。

### 搭建网站框架
1. 使用django-admin 工具创建项目文件夹
2. 使用manager.py创建一个应用
3. 在项目配置文件（settings.py）中注册应用
4. 为应用分配url

### 创建项目
```
django-admin startproject locallibrary
```

### 创建catalog应用
接下来，在locallibrary项目里，使用下面的命令创建catalog应用

```
python manage.py startapp catalog
```


### 注册catalog应用

既然应用已经创建好了，我们还必须在项目里注册它，以便工具在运行时它会包括在里面（比如在数据库里添加模型时）。在项目的settings里，把应用添加进INSTALLED_APPS ，就完成了注册。

打开项目设置文件 locallibrary/locallibrary/settings.py 找到  INSTALLED_APPS 列表里的定义。 如下所示，在列表的最后添加新的一行catalog.apps.CatalogConfig

```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'catalog.apps.CatalogConfig', 
]
```

### 配置数据库
sqllite
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```
mysql
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'locallibrary',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
```

注意：mysql需要安装mysqlconnect模块，并现在mysql数据库中创建出一个数据库

### 其他配置

settings.py里还包括其他的一些设置，现在只需要改变时区。
```
TIME_ZONE = 'Asia/Shanghai'
```

### 配置urlconf

打开locallibrary/locallibrary/urls.py 注意指导文字解释了一些使用URL映射器的方法。
```
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('catalog/', include('catalog.urls')),
    path('', RedirectView.as_view(url='/catalog/')),
]

```


在catalog文件夹里创建一个名为 urls.py 的文件, 添加下面的代码urlpatterns. 我们会在编写应用时添加相关式样。
```
from django.urls import path

from . import views


urlpatterns = [
    path('', views.index),
]
```

初始话数据库
```
python.exe manage.py migrate
```

### 数据库

Django 使用对象关系映射器（ORM）将Django代码中的模型定义映射到底层数据库使用的数据结构。当我们更改模型定义时，Django会跟踪更改并创建数据库迁移脚本 (in /locallibrary/catalog/migrations/) 来自动迁移数据库中的底层数据结构

当我们创建网站时，Django会自动添加一些模型供网站的管理部分使用（稍后我们会解释）。运行以下命令来定义数据库中这些模型的表（确保你位于包含 manage.py 的目录中):

```
python manage.py migrate
```
注意： 每次模型改变，都需要运行以上命令，来影响需要存储的数据结构（包括添加和删除整个模型和单个字段）

makemigrations 命令创建（但不适用）项目中安装的所有应用程序的迁移（你可以指定应用程序名称，也可以为单个项目运行迁移）
这migrate命令明确应用迁移你的数据库（Django跟踪哪些已添加到当前数据库）


## 使用模型

Django Web应用程序通过被称为model的Python对象访问和管理数据。model定义存储数据的结构，包括字段类型以及可能还有最大大小，默认值，选择列表选项，帮助文档，表单的标签文本等。model的定义与底层数据库无关—你可以选择其中一个作为项目设置的一部分。一旦你选择了要使用的数据库，你就不需要直接与之交谈—只需编写模型结构和其他代码，Django可以处理与数据库通信的所有繁琐工作。

## 设计LocalLibrary模型

在开始编写模型之前，花几分钟时间考虑我们需要存储的数据以及不同对象之间的关系。

我们知道，我们需要存储书籍的信息（标题，摘要，作者，语言，类别，ISBN），并且我们可能有多个副本.

一旦我们已经决定了我们的模型和字段，我们需要考虑它们的关联性。Django允许你来定义一对一的关联（OneToOneField），一对多（ForeignKey）和多对多（ManyToManyField）。


该图显示模型之间的关系，包括它们的多重性。多重性是图中的数字，显示可能存在于关系中的每个模型的数量（最大值和最小值）。例如，盒子之间的连接线显示书和类型相关。书模型中数字表明，一本书必须有一个或多个类别（尽可能多），而类型旁边的线的另一端的数字表明它可以有零个或更多的关联书

![img](./Chapter-08-code/pic/local_library_model_uml_v0_1.png)
             
### 模型入门

**模型定义**

模型通常在 models.py 中定义。它们是继承自 django.db.models.Model的子类， 可以包括字段，方法和元数据。下面的代码片段展示了一个 “typical” 模型，名为 MyModelName：

```
from django.db import models

class MyModelName(models.Model):
    """
    A typical class defining a model, derived from the Model class.
    """

    # Fields
    my_field_name = models.CharField(max_length=20, help_text="Enter field documentation")
    ...

    # Metadata
    class Meta: 
        ordering = ["-my_field_name"]

    # Methods
    def get_absolute_url(self):
         """
         Returns the url to access a particular instance of MyModelName.
         """
         return reverse('model-detail-view', args=[str(self.id)])
    
    def __str__(self):
        """
        String for representing the MyModelName object (in Admin site etc.)
        """
        return self.field_name

```

**字段**

模型可以有任意数量的字段，任何类型的字段—每个字段都表示我们要存储在我们的一个数据库中的一列数据。每个数据库记录（行）将由每个字段值之一组成。我们来看看例子。

```
my_field_name = models.CharField(max_length=20, help_text="Enter field documentation")
```

上面例子中单个字段叫 my_field_name ，类型为 models.CharField—这意味着这个字段将会包含字母数字字符串。使用特定的类分配字段类型，这些类决定了用于将数据存储在数据库中的记录的类型，以及从HTML表单接收到值（即构成有效值）时使用的验证标准。字段类型还可以获取参数，进一步指定字段如何存储或可以使用。在这种情况下，我们给出字段的两个参数：
+ max_length=20 — 表示此字段中值的最大长度为20个字符的状态
+ help_text="Enter field documentation" — 提供一个帮助用户的文本标签，让用户知道当前通过HTML表单输入时要提供什么值

字段名称用于在查询和模版中引用它。字段还有一个标签，通过参数verbose_name指定，默认值为大写字段的变量名的第一个字母，并用空格 替换下划线（例如 my_field_name ->My field name ，这就是默认标签）

如果模型以表单形式呈现（例如在管理站点中），则声明字段的顺序将影响其默认顺序

**字段参数**
在大多数字段，可以使用以下常用参数
+ help_text: 提供HTML表单文本提示 (e.g. i在管理站点中)
+ verbose_name: 字段标签中可读性名称，如果没有指定性，Django将从字段名称推断默认的详细名称
+ default: 该字段的默认值。这可以是值或可调用对象，在这种情况下，每次创建新纪录时都将调用该对象。
+ null: 如果是True，Django将 NULL 在数据库中存储适合的字段（一个CharField将代替一个空字符串）的空值。默认是False
+ blank: 如果True，表单中的字段被允许为空白。默认是False，这意味着表单的字段不可以未空。一般设置为NULL=True，因为如果要允许空值，你还希望数据库能够适当地表示它们。
+ choices: 这是一组字段选项。如果提供这一项，默认对应的表单部件是下拉选择框，而不是标准文本字段。
+ primary_key: 如果是True，将当前字段设置为模型的主键（主键是指定唯一标识所有不同表记录的特殊数据库列）。如果没有指定字段作为主键，则Django将自动为此添加一个字段。

**常用字段类型**
+ CharField 是用来定义短到中等长度的字段字符串。你必须指定max_length要存储的数据。
+ TextField  用于大型任意长度的字符串。你可以max_length为该字段指定一个最大值，但仅当该字段以表单显示时才会使用（不会在数据库级别强制执行）
+ IntegerField 是一个用于存储整数（整数）值的字段，用于在表单中验证输入的值为整数。
+ DateField 和 DateTimeField 用于存储／表示日期和日期／时间信息（分别是Python的datetime.date和datetime.datetime对象。这些字段具有单独参数auto_now=Ture （在每次保存模型时将该字段设置为当前日期），auto_now_add（仅设置模型首次创建时的日期）和default（设置默认日期，可以被用户覆盖）
+ EmailField 用于存储和验证电子邮件地址
+ FileField 和 ImageField 分别用于上传文件和图像（ImageField 只需添加上传的文件是图像的附加验证）。这些参数用于定义上传文件的存储方式和位置
+ AutoField 是一种 IntegerField 自动递增的特殊类型。如果你没有明确指定一个主键，则此类型的主键将自动添加到模型中。
+ ForeignKey 用于指定与另一个数据库模型的一对多关系（例如，汽车有一个制造商，但制造商可以制作许多汽车）
+ ManyToManyField 用于指定多对多 关系（例如，一本书可以有几种类别，每种类别可以包含几本书）。在我们的图书馆应用程序中，我们将使用ForeignKeys，但是可以用更复杂的方式来描述组之间的关系。这些具有参数on_delete来定义关联记录被删除时会发生什么

**元数据**

你可以通过声明 class Meta 声明模型级别的元数据 
```
class Meta:
    ordering = ["-my_field_name"]
    ...
```

此元数据的最有用功能之一是控制在查询模型类型时返回的记录的默认排序。你可以通过在ordering 属性的字段名称列表中指定匹配顺序来执行此操作，如上所示。排序将依赖字段的类型（字符串字段按字母顺序排序，而日期字段按时间顺序排序）。如上所示，你可以使用减号（-）对字段名称进行前缀，以反转排序顺序。

例如，如果我们选择默认排列这样的书单：
```
ordering = ["title", "-pubdate"]
```

书单通过标题依据-字母排序-排列，从A到Z，还有每个标题的出版日期，从最新到最旧。

**方法**

一个模型也可以有方法。

最起码，在每个模型中，你应该定义标准的Python 类方法 __str__() 来为每个对象返回一个人类可读的字符串。此字符用于表示管理站点的各个记录（以及你需要引用模型实例的任何其他位置）。通常这将返回模型中的标题或名称字段。

```
def __str__(self):
    return self.field_name
```

在Django模型中包含的另一种常用方法是get_absolute_url（），它返回一个URL，用于在网站上显示单个模型记录.
（如果你定义了该方法，那么Django 将自动在“管理站点”中添加“在站点中查看“按钮在模型的记录编辑栏）。典型示例以下

```
def get_absolute_url(self):
    """
    Returns the url to access a particular instance of the model.
    """
    return reverse('model-detail-view', args=[str(self.id)])
```

 假设你将使用URL/myapplication/mymodelname/2 来显示模型的单个记录（其中“2”是 id 特定 记录），则需要创建一个URL映射器来将响应和id传递给 “模型详细视图” （这将做出显示记录所需的工作）。以上示例中，reverse() 函数可以“反转”你的url映射器（在上诉命名为“model-detail-view” 的案例中，以创建正确格式的URL。

[models](https://docs.djangoproject.com/en/2.1/topics/db/models/)
**模型管理**

 一旦你定义了模型类，你可以使用它们来创建，更新或删除记录，并运行查询获取所有记录或特定的记录子集。当我们定义我们的视图，我们将展示给你在这个教程如何去做。

 创建和修改记录

 要创建一个记录，你可以定义一个模型实例，然后调用save()。

 ```
 # Create a new record using the model's constructor.
a_record = MyModelName(my_field_name="Instance #1")

# Save the object into the database.
a_record.save()
 ```
 如果你没有将任何字段声明为一个primary_key，新记录将自动给出一个字段名称id。保存上诉记录后，你可以查询此字段，值为1。

 你可以使用 -点-语法 访问此新记录中的字段，并更改值。你必须调用 save() 将修改后的值存储到数据库
 ```
 # Access model field values using Python attributes.
print(a_record.id) #should return 1 for the first record. 
print(a_record.my_field_name) # should print 'Instance #1'

# Change record by modifying the fields, then calling save().
a_record.my_field_name="New Instance Name"
a_record.save()
 ```
[query](https://docs.djangoproject.com/en/2.1/topics/db/queries/)

### 定义LocalLibrary模型

我们将开始为库定义模型。打开models.py（在locallibrary/catalog/中）
```
from django.db import models

# Create your models here.

```
from import语句导入models模块，模块模块包含我们的模型将继承的模型基类models.Model

**Genre model**

复制下面显示的类型模型代码并将其粘贴到models.py。此模型用于存储有关图书类别的信息（例如：文学，历史，经济。。）
我们将类型创建为模型而不是自由文本或选择列表，以便可以通过数据库管理。

```
class Genre(models.Model):
    """
    Model representing a book genre (e.g. Science Fiction, Non Fiction).
    """
    name = models.CharField(max_length=200, help_text="Enter a book genre (e.g. Science Fiction, French Poetry etc.)")
    
    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.name
```

该模型有一个CharField字段（name），用于描述类型（这限制为200个字符，并有help_text参数），在模型的最后，我们声明了一个__str __（）方法，它只返回由特定记录定义的类型的名称

**Book model**

```
from django.urls import reverse #Used to generate URLs by reversing the URL patterns

class Book(models.Model):
    """
    Model representing a book (but not a specific copy of a book).
    """
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book')
    isbn = models.CharField('ISBN',max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')
    
    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.title
    
    
    def get_absolute_url(self):
        """
        Returns the url to access a detail record for this book.
        """
        return reverse('book-detail', args=[str(self.id)])
```

书籍模型代表一般意义上的可用书籍的所有信息，但不是可用于特定物理“实例”或“副本”.该模型使用CharField来表示书的title和isbn,注意isbn如何使用第一个未命名参数将其标签指定为“ISBN”，因为默认标签将为“Isbn”.genre 是ManyToManyField，因此一本书可以有多种类型，一种类型可以有很多书。author为ForeignKey，因此每本书只有一个作者，但作者可能有很多书。在两种字段类型中，使用模型类或包含相关模型名称的字符串将相关模型类声明为第一个未命名参数。如果在引用之前尚未在此文件中定义关联的类，则必须将模型的名称用作字符串！
author字段中null = True，意思如果没有选择作者，则允许数据库存储Null值。on_delete = models.SET_NULL，如果关联的作者记录被删除，它将把author的值设置为Null。

该模型还定义__str __（），使用书籍的title字段来表示书的记录，get_absolute_url（）返回一个可用于访问此模型的详细记录的URL（为此，我们必须定义具有名称book-detail的URL映射，并定义关联的视图和模板）。



 

**BookInstance model**

BookInstance表示某人可能借阅的特定的一本书，并包含改书是否可借阅、预期返回的日期、版本信息、唯一id等

```
import uuid # Required for unique book instances

class BookInstance(models.Model):
    """
    Model representing a specific copy of a book (i.e. that can be borrowed from the library).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular book across whole library")
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True) 
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Book availability')

    class Meta:
        ordering = ["due_back"]
        

    def __str__(self):
        """
        String for representing the Model object
        """
        return '{0} ({1})'.format(self.id,self.book.title)
```
+ id UUIDField用于id字段，将其设置为此模型的primary_key。这种类型的字段为每个实例分配一个全局唯一值
+ book ForeignKey用于识别关联的书籍（每本书可以有多个副本，但副本只能有一本书）
+ imprint CharField代表书的特定版本
+ due_back DateField 可借阅日期（在借阅或维护之后，预计该书将可借阅的日期）此值可以为null。Class Meta 使用此字段在查询中返回记录时对记录进行排序。
+ status CharField定义一个下拉列表，我们定义一个包含键值对元组的元组，并将其传递给choices参数.键/值对中的值是用户可以选择的显示值，而键是在选择选项时实际保存的值.我们还设置了default 为'm'（维护），因为在书架上放置书籍之前，它们最初将被创建为不可用。
+ __str __（）使用其唯一ID和关联的Book的标题的组合来表示BookInstance对象。

**Author model**

```
class Author(models.Model):
    """
    Model representing an author.
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ["last_name","first_name"]
    
    def get_absolute_url(self):
        """
        Returns the url to access a particular author instance.
        """
        return reverse('author-detail', args=[str(self.id)])
    

    def __str__(self):
        """
        String for representing the Model object.
        """
        return '{0}, {1}'.format(self.last_name,self.first_name)
```

该模型将作者定义为具有名字，姓氏，出生日期和死亡日期(可选)， __str__() 返回单条记录的名称，get_absolute_url() 方法，返回作者详细信息URL映射以获取用于显示单个作者的URL。class Meta ordering定义返回一个查询集时的排序

使用django shell
搜索记录

 你可以使用模型的 objects（基类提供）搜索符合特定条件的记录。

 我们通过 QuerySet 获取一个模型的所有记录，使用 object.all()。这个QuerySet是个可迭代的对象，意味着它包括一些可以迭代/循环的对象。

 ```
 all_books = Book.objects.all()
 ```

 Django的 filter() 方法允许我们根据特定的标准过滤 返回QuerySet 的匹配指定的文本或数字字段。例如，要过滤在标题包含 “wild”和对其计数，我们可以像下面那样做。

 ```
wild_books = Book.objects.filter(title__contains='wild')
number_wild_books = Book.objects.filter(title__contains='wild').count()
 ```
注意： 双下划线和大写敏感

在某些情况下，你需要去过滤—定义了一对多关系到另一个模型的字段。在这种情况下，你可以使用附加双重下划线在相关模型中"索引"字段。例如，过滤特定类型模式的书，你将不得不索引类型字段名，如下：

```
books_containing_genre = Book.objects.filter(genre__name__icontains='fiction')
```
Book 所管关联的Genre模型中，字段名为name的字段值中包含fiction字符串的
注意：icontains忽略大小写，contains 区分大小写

### 重新运行数据库迁移
```
python manage.py makemigrations
python manage.py migrate
```

### 练习
想一下，书有很多种语言中文，英语，法语。。。如何体现出书的语言？
+ 我们需要添加一个新的模型language
+ 关联到Book模型


```
class Language(models.Model):
    """
    Model representing a Language (e.g. English, French, Japanese, etc.)
    """
    name = models.CharField(max_length=200, help_text="Enter a the book's natural language (e.g. English, French, Japanese etc.)")
    
    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.name

Book模型添加
language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)
```
 
## django admin
现在我们已经为LocalLibrary网站创建了模型，我们将使用Django Admin网站添加一些“真实”的图书数据，首先，我们来看如何使用管理站点注册模型，然后来看如何登录和创建一些数据。在最后，我们将展示一些可以进一步改进Admin站点演示的方法

Django管理应用程序可以使用你的模型自动构建可用于创建，查看，更新和删除记录的站点区域，这可以在开发过程中节省大量时间，使您可以非常轻松地测试模型并了解您是否拥有正确的数据。管理应用程序还可用于管理生产中的数据，具体取决于网站的类型。Django项目建议仅用于内部数据管理（即仅供管理员或组织内部人员使用），因为以模型为中心的方法不一定是所有用户最好的界面，并且暴露了大量不必要的细节关于模型。

### Registering models

首先，在应用程序(/locallibrary/catalog/admin.py)的目录中打开 admin.py 。如果它目前看起来像这样,注意它已经导入：django.contrib.admin
```
from django.contrib import admin

# Register your models here.

```

导入models
```
from .models import Author, Genre, Book, BookInstance,Language

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(BookInstance)
admin.site.register(Language)
```
###  创建一个superuser
要登录管理站点，我们需要一个启用了员工状态的用户帐户。为了查看和创建记录，我们还需要此用户具有管理所有对象的权限。可以使用manage.py创建具有对站点的完全访问权限和所有所需权限的“超级用户”帐户

```
python manage.py createsuperuser
```

### 高级配置
Django使用注册模型中的信息创建基本管理站点做得非常好
+ 每个模型都有一个单独的记录列表，由使用模型的__str __（）方法创建的字符串标识，并链接到详细视图/表单以进行编辑,默认情况下，此视图在顶部有一个操作菜单，可用于对记录执行批量删除操作.
+ 用于编辑和添加记录的模型详细记录表单包含模型中的所有字段，这些字段按其声明顺序垂直排列

你可以进一步自定义界面，使其更易于使用。你可以做的一些事情是
+ List views
  + 添加为每条记录显示的其他字段/信息
  + 添加过滤器以根据日期或某些其他选择值（例如，借阅状态）选择列出的记录
  + 将其他选项添加到列表视图中的操作菜单，并选择此菜单在表单上的显示位置
+ Detail views
  + 选择要显示（或排除）的字段及其顺序，分组，是否可编辑，使用的小部件，方向等。
  + 将相关字段添加到记录以允许内联编辑（例如，在创建作者记录时添加添加和编辑书籍记录的功能）

**Register a ModelAdmin class**

要更改模型在管理界面中的显示方式，请定义ModelAdmin类（描述布局）并将其注册到模型中
让我们从Authour模型开始。在应用程序目录中打开admin.py（/locallibrary/catalog/admin.py）。注释Authour模型的注册：

```
# admin.site.register(Author)
```

现在添加一个新的AuthorAdmin和注册，如下所示
```
# Define the admin class
class AuthorAdmin(admin.ModelAdmin):
    pass

# Register the admin class with the associated model
admin.site.register(Author, AuthorAdmin)
```
现在我们将为Book和BookInstance添加ModelAdmin类。我们再次需要注释掉注册
```
#admin.site.register(Book)
#admin.site.register(BookInstance)
```
现在创建并注册新模型;为了演示的目的，我们将使用@register装饰器来注册模型（这与admin.site.register（）语法完全相同）：

```
# Register the Admin classes for Book using the decorator

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    pass

# Register the Admin classes for BookInstance using the decorator

@admin.register(BookInstance) 
class BookInstanceAdmin(admin.ModelAdmin):
    pass
```

目前我们所有的管理类都是空的，因此django-admin行为将保持不变！我们现在可以扩展它们来定义我们特定于模型的管理行为

**Configure list views**

对于Authour模型localLibrary当前列出了使用从模型__str __()方法生成的对象名称的所有authour,当你只有一些作者时这很好，但是一旦你有很多作者，你可能会有重复。要区分它们，或者仅仅因为想要显示有关每个作者的更多有趣信息，你可以使用list_display向视图添加其他字段

```
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
```

对于我们的Book模型，我们还将显示author和类别
```
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
```
遗憾的是，我们无法直接在list_display中指定类型字段，因为它是ManyToManyField。我们将定义一个display_genre函数来将信息作为字符串获取

将以下代码添加到Book模型（models.py）中。这将从类型字段的前三个值（如果存在）创建一个字符串，并创建一个short_description，管理站点列中显示列名。

```
def display_genre(self):
        """
        Creates a string for the Genre. This is required to display genre in Admin.
        """
        return ', '.join([ genre.name for genre in self.genre.all()[:3] ])
    display_genre.short_description = 'Genre'
```
**Add list filters**

一旦列表中有很多记录，就可以过滤显示哪些记录。这是通过列出list_filter属性中的字段来完成的。用下面的代码片段替换当前的BookInstanceAdmin类

```
list_filter = ('status', 'due_back')
```

**Detail view**

默认情况下，详细视图按照其在模型中声明的顺序垂直排列所有字段。你可以更改声明的顺序，哪些字段显示（或排除），区段是否用于组织信息，字段是水平还是垂直显示，甚至是管理窗体中使用的编辑窗口小部件

**控制哪些字段被显示和布局**
更新您的  AuthorAdmin 类，如下所示：
```
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
```

fields控制表单上显示字段的顺序，表单中的字段默认按model中的顺序列出，定义fields后按fields里面的顺序列出。
字段默认垂直显示，但是多个字段放在元组中后，多个字段展示在一行

** 将详细视图分为多个部分**

在  BookInstance详细视图中，我们将name，imprint，id和status，due_back分成两部分.每个部分都有自己的标题,None为空标题

```
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_filter = ('status', 'due_back')
    
    fieldsets = (
        (None, {
            'fields': ('book','imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back')
        }),
    )
```

**内联编辑**
```
class BooksInstanceInline(admin.TabularInline):
    model = BookInstance

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BooksInstanceInline]
```

