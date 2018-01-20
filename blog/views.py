from urllib.parse import quote_plus

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .forms import PostForm
from .models import Post


def all_tags():
    tags = []
    for post in Post.objects.all():
        tags += post.tags.all()
    tags = list(set(tags))
    return tags


@login_required
def redirect_home(request):
    return HttpResponseRedirect("/")


@login_required
def add_tag(request, slug, tag=None):
    if not request.user.studente.is_rapistituto and not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
    instance.tags.add(tag)

    return redirect("blog:detail", instance.slug)


@login_required
def remove_tag(request, slug, tag):
    if request.user.studente.is_rapistituto or request.user.is_superuser:
        instance = get_object_or_404(Post, slug=slug)
        instance.tags.remove(tag)
        next = request.GET.get("next")
        return redirect(next)
    else:
        raise Http404


@login_required
def post_create(request):
    if request.user.studente.is_rapistituto or request.user.is_superuser:
        form = PostForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            messages.success(request, "Post Aggiunto")
            return HttpResponseRedirect(instance.get_absolute_url())
        context = {
            "form": form,
        }
        return render(request, "blog/post_form.html", context)
    else:
        raise Http404


@login_required
def post_detail(request, slug=None):
    if not request.user.studente.is_attivato:
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
    if instance.publish > timezone.now().date() or instance.draft:
        if not request.user.studente.is_rapistituto and not request.user.is_superuser:
            raise Http404

    share_string = quote_plus(instance.content)
    context = {
        "title": instance.title,
        "instance": instance,
        "share_string": share_string,
        "tags": all_tags(),
    }
    return render(request, "blog/post_detail.html", context)


@login_required
def post_list(request):
    if not request.user.studente.is_attivato:
        raise Http404
    today = timezone.now().date()
    filtro = "-publish"
    queryset_list = Post.objects.filter(draft=False, publish__lte=today).order_by(filtro)
    if request.user.studente.is_rapistituto or request.user.is_superuser:
        queryset_list = Post.objects.all().order_by(filtro)

    query = request.GET.get("q")
    next = request.GET.get("next")
    tag = request.GET.get("tag")

    if query:
        if ' ' in query:
            queryset_list = queryset_list.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(user__first_name__iexact=query.split(' ')[0]) &
                Q(user__last_name__iexact=query.split(' ')[1]) |
                Q(user__first_name__iexact=query.split(' ')[1]) &
                Q(user__last_name__iexact=query.split(' ')[0])
            ).distinct()
        else:
            queryset_list = queryset_list.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query)
            ).distinct()

    if tag:
        queryset_list = queryset_list.filter(tags__name__in=[tag])

    paginator = Paginator(queryset_list, 5)
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    context = {
        "object_list": queryset,
        "title": "Comunicazioni",
        "page_request_var": page_request_var,
        "today": today,
        "tags": all_tags(),
        "next": next,
    }
    return render(request, "blog/post_list.html", context)


@login_required
def post_update(request, slug=None):
    if not request.user.studente.is_rapistituto and not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Post Salvato", extra_tags='html_safe')
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": instance.title,
        "instance": instance,
        "form": form,
    }
    return render(request, "blog/post_form.html", context)


@login_required
def post_delete(request, slug=None):
    if not request.user.studente.is_rapistituto and not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
    instance.delete()
    messages.success(request, "Post Cancellato")
    return HttpResponseRedirect("/")
