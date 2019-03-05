from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from .models import Comment
from .forms import CommentForm
from blog.models import Post

def post_comment(request, post_pk):
	post = get_object_or_404(Post, pk=post_pk)
	# 只有请求方式为post时，才需要处理表单
	if request.method == 'POST':
		# 用户提交的数据存在request.POST中，这是一个类字典对象
		# 因此，只有当用户请求为post时，才需要处理表单数据
		form = CommentForm(request.POST)
		# 检查表单合法性
		if form.is_valid():
			# 检查表单合法，调用save()方法，保存到数据库
			# commit=False：仅仅利用表单数据生成Comment模型实例，但不保存评论数据到数据库
			comment = form.save(commit=False)
			# 关联文章和文章评论
			comment.post = post
			# 将评论保存进数据库
			comment.save()
			# 重定向到 post 的详情页，实际上当 redirect 函数接收一个模型的实例时，
			# 它会调用这个模型实例的 get_absolute_url 方法，
            # 然后重定向到 get_absolute_url 方法返回的 URL。
			return redirect(post)
		else:
			# 检查到数据不合法，重新渲染详情页，并且渲染表单的错误。
			# post.comment_set.all()：获取和这个post关联的全部评论
			comment_list = post.comment_set.all()
			context = {'post': post,
						'form': form,
						'comment_list': comment_list
			}
			return render(request, 'blog/detail.html', context=context)

	return redirect(post)