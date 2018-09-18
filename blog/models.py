from django.db import models

# Create your models here.

"""
设计博客的数据库表结构
博客最主要的功能就是展示我们写的文章，它需要从某个地方获取博客文章数据才能把文章展示出来，通常来说这个地方就是数据库。我们把写好的
文章永久地保存在数据库里，当用户访问我们的博客时，Django 就去数据库里把这些数据取出来展现给用户。

博客的文章应该含有标题、正文、作者、发表时间等数据。一个更加现代化的博客文章还希望它有分类、标签、评论等。为了更好地存储这些数据，
我们需要合理地组织数据库的表结构。

我们的博客初级版本主要包含博客文章，文章会有分类以及标签。一篇文章只能有一个分类，但可以打上很多标签。

数据库存储的数据其实就是表格的形式，例如存储博客文章的数据库表长这个样子：

文章 id	标题	正文	发表时间	分类	标签
1	title 1	text 1	2016-12-23	Django	Django 学习
2	title 2	text 2	2016-12-24	Django	Django 学习
3	title 3	text 3	2016-12-26	Python	Python 学习
其中文章 ID 是一个数字，唯一对应着一篇文章。当然还可以有更多的列以存储更多相关数据，这只是一个最基本的示例。

数据库表设计成这样其实已经可以了，但是稍微分析一下我们就会发现一个问题，这 3 篇文章的分类和标签都是相同的，这会产生很多重复数据，
当数据量很大时就浪费了存储空间。

不同的文章可能它们对应的分类或者标签是相同的，所以我们把分类和标签提取出来，做成单独的数据库表，再把文章和分类、标签关联起来。
下面分别是分类和标签的数据库表：

分类 id	分类名
1	Django
2	Python
标签 id	标签名
1	Django 学习
2	Python 学习
"""

from django.contrib.auth.models import User


class Category(models.Model):
    """
    Django 要求模型必须继承 models.Model 类。
    Category 只需要一个简单的分类名 name 就可以了。
    CharField 指定了分类名 name 的数据类型，CharField 是字符型，
    CharField 的 max_length 参数指定其最大长度，超过这个长度的分类名就不能被存入数据库。
    当然 Django 还为我们提供了多种其它的数据类型，如日期时间类型 DateTimeField、整数类型 IntegerField 等等。
    Django 内置的全部类型可查看文档：
    https://docs.djangoproject.com/en/1.10/ref/models/fields/#field-types
    """
    name = models.CharField(max_length=100)


class Tag(models.Model):
    """
    标签 Tag 也比较简单，和 Category 一样。
    再次强调一定要继承 models.Model 类！
    """
    name = models.CharField(max_length=100)


class Post(models.Model):
    """
    文章的数据库表稍微复杂一点，主要是涉及的字段更多。
    """

    # 文章标题
    title = models.CharField(max_length=70)

    # 文章正文，我们使用了 TextField。
    # 存储比较短的字符串可以使用 CharField，但对于文章的正文来说可能会是一大段文本，因此使用 TextField 来存储大段文本。
    body = models.TextField()

    # 这两个列分别表示文章的创建时间和最后一次修改时间，存储时间的字段用 DateTimeField 类型。
    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()

    # 文章摘要，可以没有文章摘要，但默认情况下 CharField 要求我们必须存入数据，否则就会报错。
    # 指定 CharField 的 blank=True 参数值后就可以允许空值了。
    excerpt = models.CharField(max_length=200, blank=True)

    # 这是分类与标签，分类与标签的模型我们已经定义在上面。
    # 我们在这里把文章对应的数据库表和分类、标签对应的数据库表关联了起来，但是关联形式稍微有点不同。
    # 我们规定一篇文章只能对应一个分类，但是一个分类下可以有多篇文章，所以我们使用的是 ForeignKey，即一对多的关联关系。
    # 而对于标签来说，一篇文章可以有多个标签，同一个标签下也可能有多篇文章，所以我们使用 ManyToManyField，表明这是多对多的关联关系。
    # 同时我们规定文章可以没有标签，因此为标签 tags 指定了 blank=True。
    # 如果你对 ForeignKey、ManyToManyField 不了解，请看教程中的解释，亦可参考官方文档：
    # https://docs.djangoproject.com/en/1.10/topics/db/models/#relationships
    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag, blank=True)

    # 文章作者，这里 User 是从 django.contrib.auth.models 导入的。
    # django.contrib.auth 是 Django 内置的应用，专门用于处理网站用户的注册、登录等流程，User 是 Django 为我们已经写好的用户模型。
    # 这里我们通过 ForeignKey 把文章和 User 关联了起来。
    # 因为我们规定一篇文章只能有一个作者，而一个作者可能会写多篇文章，因此这是一对多的关联关系，和 Category 类似。
    author = models.ForeignKey(User)