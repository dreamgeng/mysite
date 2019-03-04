from django.shortcuts import render

# Create your views here.
from .models import Post, Category
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
import markdown
from comments.forms import CommentForm

# 这个 request 就是 Django 为我们封装好的 HTTP 请求，它是类 HttpRequest 的一个实例
def index(request):
	# post_list = Post.objects.all().order_by('-created_time')
	post_list = Post.objects.all()
	print(post_list)
	return render(request, 'blog/index.html', context={
		'title':'dreamgeng',
		'welcome':'welcome to myblog!',
		# 'post_list': post_list
		'post_list': post_list

		})

def detail(request, pk):
	post = get_object_or_404(Post, pk=pk)
	post.body = markdown.markdown(post.body,
								extensions=[
								'markdown.extensions.extra',
								'markdown.extensions.codehilite',
								'markdown.extensions.toc',

								])
	form = CommentForm()
	comment_list = post.comment_set.all()
	context = {'post': post,
				'form': form,
				'comment_list': comment_list
	}
	return render(request, 'blog/detail.html', context=context)

def archives(request, year, month):
	post_list = Post.objects.filter(created_time__year=year,
		created_time__month=month
		).order_by('-created_time')
	return render(request, 'blog/index.html', context={'post_list': post_list})

def category(request, pk):
	cate = get_object_or_404(Category, pk=pk)
	post_list = Post.objects.filter(category=cate).order_by('-created_time')
	return render(request, 'blog/index.html', context={'post_list': post_list})