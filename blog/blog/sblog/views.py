#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from django.shortcuts import render_to_response
from django.http import Http404
from blog.sblog.models import Blog
from blog.sblog.models import Tag
from django.http import HttpResponseRedirect
from django.template import RequestContext
from blog.sblog.models import Author
from blog.sblog.forms import BlogForm
from blog.sblog.forms import TagForm
from blog.utils.tools import log


def blog_add(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        tag = TagForm(request.POST)
        if form.is_valid() and tag.is_valid():
            cd = form.cleaned_data
            cdtag = tag.cleaned_data
            tagname = cdtag['tag_name']
            for taglist in tagname.split():
                log(33333)
                log(taglist)
                Tag.objects.get_or_create(tag_name=taglist.strip())
            title = cd['caption']
            author = Author.objects.get(id=1)
            content = cd['content']
            blog = Blog(caption=title, author=author, content=content)
            blog.save()
            for taglist in tagname.split():
                blog.tags.add(Tag.objects.get(tag_name=taglist.strip()))
                blog.save()
            id = Blog.objects.order_by('-publish_time')[0].id
            return HttpResponseRedirect('/sblog/blog/%s' % id)
    else:
        form = BlogForm()
        tag = TagForm(initial={'tag_name': 'notags'})
    return render_to_response('blog_add.html',
        {'form': form, 'tag': tag}, context_instance=RequestContext(request))


def blog_filter(request, id=''):
    tags = Tag.objects.all()
    tag = Tag.objects.get(id=id)
    blogs = tag.blog_set.all()
    return render_to_response("blog_filter.html",
        {"blogs": blogs, "tag": tag, "tags": tags})


def blog_show(request, id=''):
    try:
        blog = Blog.objects.get(id=id)
    except Blog.DoesNotExist:
        raise Http404
    return render_to_response("sblog/blog_show.html", {"blog": blog})


def blog_list(request):
    blogs = Blog.objects.all()
    return render_to_response("sblog/blog_list.html", {"blogs": blogs})