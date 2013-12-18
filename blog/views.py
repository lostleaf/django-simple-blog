# Create your views here.
from django.shortcuts import render_to_response
from blog.models import *
from blog.forms import *
from django.http import Http404
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User

def blog_list(request):
  """docstring for blog_list"""
  blogs = Blog.objects.all()
  tags  = Tag.objects.all()
  htext = "Blogs"
  return render_to_response("blog_list.html", 
    {"blogs": blogs, "htext": htext, "tags": tags, "user": request.user})

def blog_show(request, id = ''):
 """docstring for blog_show"""
 try:
   blog = Blog.objects.get(id = id)
 except Blog.DoesNotExist:
   raise Http404
 return render_to_response("blog_show.html", {"blog": blog, "user": request.user})

def home(request):
  """docstring for home"""
  latest = Blog.objects.order_by("-publish_time")[0:3]
  return render_to_response("home.html", {"latest": latest})

def search(request):
  key   = request.GET.get('q')
  blogs = Blog.objects.filter(Q(caption__icontains=key) | Q(content__icontains=key))
  tags  = Tag.objects.all()
  htext = "Search"
  return render_to_response("blog_list.html", {"blogs": blogs, "htext": htext, "tags": tags})

def search_tag(request, id = ''):
  tag   = Tag.objects.get(id = id)
  tags  = Tag.objects.all()
  blogs = tag.blog_set.all()
  htext = "Search by Tag"
  return render_to_response("blog_list.html", {"blogs": blogs, "htext": htext, "tags": tags})

def blog_add(request):
  if request.method == 'POST':
    form = BlogForm(request.POST)
    tag  = TagForm(request.POST)
    if form.is_valid() and tag.is_valid():
      data     = form.cleaned_data
      data_tag = tag.cleaned_data
      tagname  = data_tag['tag_name']
      for taglist in tagname.split():
        Tag.objects.get_or_create(tag_name = taglist.strip())
      title    = data['caption']
      author   = Author.objects.get(id=1)
      content  = data['content']
      blog     = Blog(caption=title, author=author, content=content)
      blog.save()
      for taglist in tagname.split():
        blog.tags.add(Tag.objects.get(tag_name = taglist.strip()))
        blog.save()
      id       = Blog.objects.order_by('-publish_time')[0].id
      return HttpResponseRedirect('/blog/blog/%s' % id)
  
  form = BlogForm()
  tag  = TagForm()
  return render_to_response('blog_add.html', {'form': form, 'tag': tag}, 
                            context_instance=RequestContext(request))

def blog_update(request, id=""):
  id = id
  if request.method == 'POST':
    form = BlogForm(request.POST)
    tag = TagForm(request.POST)
    if form.is_valid() and tag.is_valid():
      cd = form.cleaned_data
      cdtag = tag.cleaned_data
      tagname = cdtag['tag_name']
      tagnamelist = tagname.split()
      for taglist in tagnamelist:
        Tag.objects.get_or_create(tag_name=taglist.strip())
      title = cd['caption']
      content = cd['content']
      blog = Blog.objects.get(id=id)
      if blog:
        blog.caption = title
        blog.content = content
        blog.save()
        for taglist in tagnamelist:
          blog.tags.add(Tag.objects.get(tag_name=taglist.strip()))
          blog.save()
        tags = blog.tags.all()
        for tagname in tags:
          tagname = unicode(str(tagname), "utf-8")
          if tagname not in tagnamelist:
            notag = blog.tags.get(tag_name=tagname)
            blog.tags.remove(notag)
      else:
        blog = Blog(caption=blog.caption, content=blog.content)
        blog.save()
      return HttpResponseRedirect('/blog/blog/%s' % id)

  try:
      blog = Blog.objects.get(id=id)
  except Exception:
      raise Http404
  form = BlogForm(initial={'caption': blog.caption, 'content': blog.content})
  tags = blog.tags.all()
  if tags:
      taginit = ''
      for x in tags:
          taginit += str(x) + ' '
      tag = TagForm(initial={'tag_name': taginit})
  else:
      tag = TagForm()
  return render_to_response('blog_add.html',
      {'blog': blog, 'form': form, 'id': id, 'tag': tag},
      context_instance=RequestContext(request))

def blog_del(request, id=""):
  try:
    blog = Blog.objects.get(id=id)
  except Exception:
    raise Http404
  if blog:
    blog.delete()
    return HttpResponseRedirect("/blog/")
  blogs = Blog.objects.all()
  return render_to_response("blog_list.html", {"blogs": blogs})

def login(request):
  if request.method == 'POST':
    form = LoginForm(request.POST)
    if form.is_valid():
      data = form.cleaned_data
      user=authenticate(username=data['username'],password=data['password'])
      auth_login(request, user)
      return HttpResponseRedirect("/blog/")

  form = LoginForm()
  return render_to_response('login.html', {'form': form}, context_instance=RequestContext(request))

def logout(request):
  auth_logout(request)
  return HttpResponseRedirect("/blog/")