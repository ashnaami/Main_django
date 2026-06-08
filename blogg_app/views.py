from django.shortcuts import render
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from .models import TB_User, TB_Post, TB_Comments, TB_Like
from .serializer import RegisterSerializer, PostSerializer, CommentSerializer
from rest_framework import status
import os
from dotenv import load_dotenv
from openai import OpenAI
from rest_framework.parsers import MultiPartParser, FormParser
# from rest_framework import generics

# Create your views here.

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

@api_view(['POST'])
def register(request):
    print("DATA:", request.data)
    serializer = RegisterSerializer(data=request.data)
    if serializer .is_valid():
        serializer.save()
        return Response({'message' : 'registration successfull'}, status=status.HTTP_201_CREATED)
    print("ERRORS:", serializer.errors)

    return Response(serializer.errors)

@api_view(['POST'])
def login(request):

    email = request.data.get("email")
    password = request.data.get("password")

    print("EMAIL:", email)
    print("PASSWORD:", password)

    try:
        user = TB_User.objects.get(email=email)

        print("USER FOUND:", user.email)
        print("DB PASSWORD:", user.password)

        if user.password == password:

            return Response({
                "id": user.id,
                "name": user.name,
                "email": user.email
            })

        return Response(
            {"message": "Wrong Password"},
            status=status.HTTP_400_BAD_REQUEST
        )
    except TB_User.DoesNotExist:
        print("EMAIL NOT FOUND")
        return Response(
            {"message": "Email Not Found"},
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['GET'])
def view_profile(request, id):
    try:
        user = TB_User.objects.get(id=id)
        posts = TB_Post.objects.filter(user_id=id)
        post_list = []

        for post in posts:
            likes_count = TB_Like.objects.filter(post_id=post.id).count()
            comments = TB_Comments.objects.filter(post_id=post.id)
            comment_list = []

            for c in comments:
                comment_list.append({
                    "id": c.id,
                    "comment": c.comments 
                })
            post_list.append({
                "id": post.id,
                "title": post.title,
                "description": post.description,
                "category": post.category,
                "likes": likes_count,
                "comments": comment_list
            })
        return Response({
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "phone": getattr(user, "phone", "")
            },
            "posts": post_list
        })
    except TB_User.DoesNotExist:
        return Response({"message": "User not found"}, status=404)
    except Exception as e:
        import traceback
        print(traceback.format_exc())  
        return Response({"error": str(e)}, status=500)
    
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def add_post(request):
    try:
        user = TB_User.objects.get(id=request.data["user"])
        post = TB_Post.objects.create(user=user,title=request.data["title"],description=request.data["description"],category=request.data["category"],image=request.FILES.get("image"))
        return Response({"message": "Post created successfully"})

    except Exception as e:
        return Response({"error": str(e)}, status=400)
@api_view(['GET'])
def single_post(request, id):
    post = TB_Post.objects.get(id=id)
    serializer = PostSerializer(post)
    return Response(serializer.data)

@api_view(['GET'])
def view_post(request):
    posts= TB_Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_post(request, id):
    try:
        post = TB_Post.objects.get(id=id)
        serializer = PostSerializer(post)
        return Response(serializer.data)
    except TB_Post.DoesNotExist:
        return Response({"error": "Post not found"}, status=404)



@api_view(['PUT'])
@parser_classes([MultiPartParser, FormParser])
def edit_post(request, id):
    try:
        post = TB_Post.objects.get(id=id)
    except TB_Post.DoesNotExist:
        return Response({"error": "Post not found"}, status=404)
    serializer = PostSerializer(post, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    print("ERRORS:", serializer.errors)
    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
def delete_post(request,id):
    posts=TB_Post.objects.get(id=id)
    posts.delete()
    return Response({'message':'deleted'},status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def comments(request):
    serializer = CommentSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save() 
        return Response({'message': 'comment added'}, status=201)    
    print("Serializer Errors:", serializer.errors)  
    return Response(serializer.errors, status=400)


@api_view(['GET'])
def view_comments(request, id):
    comments = TB_Comments.objects.filter(post_id=id)  # 🔥 FIX
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def content_helper(request):

    text = request.data.get("text")

    if not text:
        return Response({"error": "No text provided"}, status=400)

    response = client.responses.create(
        model="gpt-5.4-mini",
        input=f"""
        Fix grammar, spelling, punctuation, and capitalization errors in the text.
        If the text is a topic or title, generate a clear and engaging paragraph about it.
        If the text is already a paragraph, improve its readability and sentence structure while preserving its original meaning.
        Add relevant details and useful information related to the topic to make the content more informative.
        Use simple, easy-to-understand language suitable for blog readers.
        Return only the final improved content without explanations.
        User Input:
        {text}
        """
    )
    return Response({
        "result": response.output_text
    })

@api_view(['GET'])
def search_posts(request):

    category = request.GET.get('category', '')

    posts = TB_Post.objects.filter(
        category__contains=category
    )

    serializer = PostSerializer(posts, many=True)

    return Response(serializer.data)


@api_view(['POST'])
def like_post(request, id):
    user_id = request.data.get("user")
    post = TB_Post.objects.get(id=id)
    already_liked = TB_Like.objects.filter(user=user_id, post=post).exists()

    if already_liked:
        return Response({"message": "Already liked"})

    TB_Like.objects.create(user_id=user_id,post=post)

    return Response({"likes": TB_Like.objects.filter(post=post).count()})

@api_view(['GET'])
def like_count(request, id):

    count = TB_Like.objects.filter(
        post_id=id
    ).count()

    return Response({
        "likes": count
    })

