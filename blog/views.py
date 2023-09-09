from django.shortcuts import render,HttpResponse,redirect
from blog.models import Post,BlogComment
from django.contrib import messages 
from django.contrib.auth.models import User
# from django.templatetags import extra
# Create your views here.


def blogHome(request):
    allPosts=Post.objects.all()
    context={"allPosts":allPosts}
    return render(request,"blog/blogHome.html",context)

def blogPost(request,slug):
    post=Post.objects.filter(slug=slug).first()
    post.views=post.views+1
    post.save()
    comments=BlogComment.objects.filter(post=post,parent=None)
    replies=BlogComment.objects.filter(post=post).exclude(parent=None)
    repDict={}
    for reply in replies:
        if reply.parent.sno not in repDict.keys():
            repDict[reply.parent.sno]=[reply]
        else:
            repDict[reply.parent.sno].append(reply)
    
    # print(comments,replies)
    # print(repDict)
    context={"post":post,'comments':comments, "user":request.user,"repDict":repDict}
    return render(request,"blog/blogPost.html",context)

# API 
def postComment(request):
    if request.method=='POST':
        comment=request.POST.get('comment')
        user=request.user
        postsno=request.POST.get('postsno')
        parentsno=request.POST.get('parentsno')
        post=Post.objects.get(sno=postsno)
        if parentsno=="":
            comment=BlogComment(comment=comment,user=user,post=post)
            comment.save()
            messages.success(request,"Your Comment has been Posted Successfully")
        else:
            parent=BlogComment.objects.get(sno=parentsno)
            comment=BlogComment(comment=comment,user=user,post=post,parent=parent)
            comment.save()
            messages.success(request,"Your Reply has been Posted Successfully")

    return redirect(f'/blog/{post.slug}')