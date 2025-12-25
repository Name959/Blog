from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.core.paginator import Paginator # 引入分页器

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

def index(request):
    return render(request, 'blog/index.html')

@login_required
def topics(request):
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'blog/topics.html', context)

@login_required
def topic(request, topic_id):
    # 使用 get_object_or_404 简化代码，效果等同于 try-except Http404
    topic = get_object_or_404(Topic, id=topic_id)
    
    # 确认请求的用户是主题的所有者
    if topic.owner != request.user:
        raise Http404

    # 获取该主题下的所有条目，按时间降序排列
    entries_list = topic.entry_set.order_by('-date_added')
    
    # 分页设置：每页显示 5 个条目
    paginator = Paginator(entries_list, 5) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # 将 page_obj 传递给模板，它包含了当前页数据和分页信息
    context = {'topic': topic, 'page_obj': page_obj}
    return render(request, 'blog/topic.html', context)

@login_required
def new_topic(request):
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('blog:topics')

    context = {'form': form}
    return render(request, 'blog/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('blog:topic', topic_id=topic_id)

    context = {'topic': topic, 'form': form}
    return render(request, 'blog/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog:topic', topic_id=topic.id)

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'blog/edit_entry.html', context)

@login_required
def delete_entry(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)
    topic = entry.topic
    
    # 安全检查：确保只有所有者可以删除
    if topic.owner != request.user:
        raise Http404
    
    entry.delete()
    return redirect('blog:topic', topic_id=topic.id)

@login_required
def delete_topic(request, topic_id):
    # 获取 topic，如果不存在则返回 404
    topic = get_object_or_404(Topic, id=topic_id)
    
    # 安全检查：确保只有所有者可以删除
    if topic.owner != request.user:
        raise Http404
    
    # 执行删除操作
    # 注意：由于 models.py 中 Entry 定义了 on_delete=models.CASCADE
    # 删除 topic 会自动删除它包含的所有 entries
    topic.delete()
    
    # 删除后重定向回 topic 列表页
    return redirect('blog:topics')