# Create your views here.
from django.shortcuts import render_to_response
from blog.models import Blog
from django.http import Http404

def blog_list(request):
  """docstring for blog_list"""
  blogs = Blog.objects.all()
  return render_to_response("blog_list.html", {"blogs": blogs})

def blog_show(request, id = ''):
 """docstring for blog_show"""
 try:
   blog = Blog.objects.get(id = id)
 except Blog.DoesNotExist:
   raise Http404
 return render_to_response("blog_show.html", {"blog": blog})

def home(request):
  """docstring for home"""
  latest = Blog.objects.order_by("-update_time")[0:3]
  return render_to_response("home.html", {"latest": latest})
