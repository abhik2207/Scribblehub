from django.shortcuts import render, HttpResponse, redirect
from .models import Post, BlogComment
from django.contrib import messages

# Create your views here.
def blogHome(request):
    allPosts = Post.objects.all()
    return render(request, "blog/blogHome.html", {'allPosts':allPosts})


def blogPost(request, slug):
    post = Post.objects.filter(slug=slug).first()
    post.views = post.views + 1
    post.save()
    comments = BlogComment.objects.filter(post=post, parent=None)
    replies = BlogComment.objects.filter(post=post).exclude(parent=None)
    replyDict = {}
    for reply in replies:
        if reply.parent.s_no not in replyDict.keys():
            replyDict[reply.parent.s_no] = [reply]
        else:
            replyDict[reply.parent.s_no].append(reply)
    return render(request, "blog/blogPost.html", {'post': post, 'comments':comments, 'user':request.user, 'replyDict':replyDict})

def postComment(request):
    if request.method=="POST":
        comment = request.POST.get('comment')
        user = request.user
        postSno = request.POST.get('postSno')
        post = Post.objects.get(post_no=postSno)
        parentSno = request.POST.get('parentSno')
        if parentSno == "":
            blogComment = BlogComment(comment=comment, user=user, post=post)
            blogComment.save()
            messages.success(request, "Your comment has been posted successfully")
        else:
            parent = BlogComment.objects.get(s_no=parentSno)
            blogComment = BlogComment(comment=comment, user=user, post=post, parent=parent)
            blogComment.save()
            messages.success(request, "Your reply has been posted successfully")
    return redirect(f'/blog/{post.slug}')
