
from django.db import models
from django.shortcuts import render,HttpResponse, get_object_or_404
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from .models import Comment, post
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy


def LikeView(request,pk):
    posts = get_object_or_404(post, id=request.POST.get('post_id'))
    liked = False
    if posts.likes.filter(id=request.user.id).exists():
        posts.likes.remove(request.user)
        liked=False
    else:
        posts.likes.add(request.user)
        liked=True
    
    return HttpResponseRedirect(reverse('post-detail',args=[str(pk)]))




class PostListView(ListView):
    model = post
    template_name = 'home/index.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

class UserPostListView(ListView):
    model = post
    template_name = 'home/user_posts.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User,username=self.kwargs.get('username'))
        return post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
    model = post
    def get_context_data(self,*args,**kwargs):
        context = super(PostDetailView, self).get_context_data(*args,**kwargs)
        stuff=get_object_or_404(post,id=self.kwargs['pk'])
        liked = False
        if stuff.likes.filter(id= self.request.user.id).exists():
            liked=True
        
        total_likes = stuff.total_likes()
        context["total_likes"] = total_likes
        context["liked"] = liked
        return context


class PostCreateView(LoginRequiredMixin,CreateView):
    model = post
    fields = ['title','content']
    

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostCommentView(CreateView):
    model = Comment
    fields = ['body']
    template_name = 'home/add_comment.html'
    #ordering = ['-date_added']
    #success_url = reverse_lazy('home')

    def form_valid(self,form):
        form.instance.name = self.request.user
        posts = post.objects.get(id=self.kwargs['pk'])
        form.instance.posts = posts
        return super().form_valid(form)
    #def get_queryset(self):
        #posts = get_object_or_404(post,id=self.kwargs['pk'])
        #return Comment.objects.filter(posts=posts).order_by('-date_added')




   

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = post
    fields = ['title','content']

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    
class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = post
    success_url = '/'
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

# Create your views here.
