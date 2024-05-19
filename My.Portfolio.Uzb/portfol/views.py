# from django.shortcuts import render
# from .models import Site, Comment, Category 
# from .serilazers import SiteSerializer, CommentSerializer, CategorySerializer, SiteApiSerializer, CommentApiSerializer, CategoryApiSerializer

# from rest_framework.response import Response
# from rest_framework import viewsets, serializers
# from rest_framework.permissions import AllowAny, IsAuthenticated
# from rest_framework.generics import RetrieveAPIView, ListAPIView


# class CategoryViewset(viewsets.ModelViewSet):
#     queryset = Category.objects.filter(status=True)
#     serializer_class = CategorySerializer
#     permission_classes = [AllowAny]


# class SiteViewset(viewsets.ModelViewSet):
#     queryset = Site.objects.filter(status=True)
#     serializer_class = SiteSerializer
#     permission_classes = [AllowAny]


# class CommentViewset(viewsets.ModelViewSet):
#     queryset = Comment.objects.filter(status=True)
#     serializer_class = CommentSerializer
#     permission_classes = [AllowAny]


# class SiteApiDetailview(RetrieveAPIView):
#     queryset = Site.objects.filter(status=True)
#     serializer_class = SiteApiSerializer
#     permission_classes = [AllowAny]
#     lookup_field = 'slug'


# class CategoryApiDetailview(RetrieveAPIView):
#     queryset = Category.objects.filter(status=True)
#     serializer_class = CategoryApiSerializer
#     permission_classes = [AllowAny]
#     lookup_field = 'slug'


# class CommentApiDetailview(RetrieveAPIView):
#     queryset = Comment.objects.filter(status=True)
#     serializer_class = CommentApiSerializer
#     permission_classes = [AllowAny]
#     lookup_field = 'slug'







from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from portfol.models import Category, Site, Comment
from .forms import ShareForm, CommentForm

from taggit.models import Tag

# Create your views here.


def listview(request, tag_slug=None):
    most_new = Site.objects.filter(status='active').first()
    last_news = Site.objects.filter(status='active')[1:7]
    sites = Site.objects.filter(status='active')
    videos = Site.objects.exclude(video__exact='').filter(status='active')[:6]

    categories = Category.objects.filter(status='active')

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        sites = sites.filter(tags__in=[tag])


    paginator = Paginator(sites, 9)
    page = request.GET.get('page')
    try:
        sites = paginator.page(page)
    except PageNotAnInteger:
        sites = paginator.page(1)
    except EmptyPage:
        sites = paginator.page(paginator.num_pages)

    context = {
        'most_new': most_new,
        'last_news': last_news,
        'saytlar': sites,
        'categories': categories,
        'videos': videos,
        'page': page,
        'tag': tag,
    }

    return render(request, 'portfol/list.html', context)


def detailview(request, id):
    site = get_object_or_404(Site, id=id)
    sites = Site.objects.filter(category=site.category, status='active')[:4]
    categories = Category.objects.filter(status='active')

    comments = site.comments.filter(status=True)

    new_comment = None
    if request.method == 'SITE':
        comment_form = CommentForm(data=request.SITE)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.site = site
            new_comment.save()
    else:
        comment_form = CommentForm()

    context = {
        'sayt': site,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
        'sites': sites,
        'categories': categories,
    }

    return render(request, 'portfol/detail.html', context)


def post_share(request, id):
    site = get_object_or_404(Site, id=id)
    categories = Category.objects.filter(status='active')
    sent = False
    print("111111111111111")
    if request.method == 'SITE':
        form = ShareForm(request.SITE)
        print("111111111111111")
        if form.is_valid():
            print("111111111111111")
            cd = form.cleaned_data

            site_url = request.build_absolute_uri(site.get_absolute_url())
            email = cd['email']
            subject = f"{cd['name']}({cd['email']}) sizga {site.title} tafsiya qildi"
            message = f"{site.title} ni quidagi link orqali o'qing: {site_url}  Comment: {cd['comment']}"
            send_mail(subject, message, email, [cd['to']])
            sent = True
            print("111111111111111")
    else:
        form = ShareForm()

    context = {'site': site, 'form': form,
               'sent': sent, 'categories': categories}

    return render(request, 'portfol/share.html', context)


def base_view(request, *args, **kwargs):
    categories = Category.objects.filter(status='active')

    context = {
        'categories': categories,
    }

    return render(request, 'base.html', context)


def category_list(request, id):
    category_object = get_object_or_404(Category, id=id)
    sites = Site.objects.filter(
        status='active', category=category_object.id)[:12]

    categories = Category.objects.filter(status='active')

    paginator = Paginator(posts, 1)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'category_object': category_object,
        'sites': sites,
        'categories': categories
    }

    return render(request, 'portfol/category_list.html', context)
