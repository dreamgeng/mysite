from django.db import models

# Create your models here.
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# 编写数据库模型代码
# Category 就是一个标准的 Python 类，
# 它继承了 models.Model 类，类名为 Category 。
# Django 要求模型必须继承 models.Model 类。
# Category 类有一个属性 name，它是 models.CharField 的一个实例。

# Django 就可以把这个类翻译成数据库的操作语言，
# 在数据库里创建一个名为 category 的表格，
# 这个表格的一个列名为 name。
# 还有一个列 id，Django 则会自动创建。
class Category(models.Model):
	# CharField 的 max_length 参数指定其最大长度，超过这个长度的分类名就不能被存入数据库。
    # 当然 Django 还为我们提供了多种其它的数据类型，
    # 如日期时间类型 DateTimeField、整数类型 IntegerField 等等。
	name = models.CharField(max_length=100)
	# 我们从数据库中取出数据后，显示的是字符串，
	# 而无法看出取出的内容，所以这里定义一个 `__str__` 方法，
	# 定义好 __str__ 方法后，解释器显示的内容将会是 __str__ 方法返回的内容。
	# 这里 Category 返回分类名 name ，Tag 返回标签名，而 Post 返回它的 title。
	def __str__(self):
		return self.name

class Tag(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name

class Post(models.Model):
	title = models.CharField(max_length=80)
	# 文章正文，我们使用了 TextField。
    # 存储比较短的字符串可以使用 CharField，
    # 但对于文章的正文来说可能会是一大段文本，因此使用 TextField 来存储大段文本。
	body = models.TextField()
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
    # 在django2.0以后，ForeignKe()中on_delete参数不可以为空，需要指定参数
    # 且　on_delete　可选参数为　CASCADE, DO_NOTHING, PROTECT, SET, SET_DEFAULT, SET_NULL
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	tags = models.ManyToManyField(Tag, blank=True)
	# 文章作者，这里 User 是从 django.contrib.auth.models 导入的。
    # django.contrib.auth 是 Django 内置的应用，专门用于处理网站用户的注册、登录等流程，User 是 Django 为我们已经写好的用户模型。
    # 这里我们通过 ForeignKey 把文章和 User 关联了起来。
    # 因为我们规定一篇文章只能有一个作者，而一个作者可能会写多篇文章，因此这是一对多的关联关系，和 Category 类似。
	author = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		# reverse 函数会去解析detail这个视图函数对应的 URL
		# detail 对应的规则就是 post/(?P<pk>[0-9]+)/ 这个正则表达式，而正则表达式部分会被后面传入的参数 pk(id)替换
		# id 是模块自带的self.pk给出的ID记录...
		return reverse('blog:detail', kwargs={'pk': self.pk})

	class Meta:
		ordering = ['-created_time']