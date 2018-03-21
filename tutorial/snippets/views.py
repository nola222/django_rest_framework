# 使用rest框架框架新组件  
# REST框架为没每个状态码(status code)提供明确的标识符，如HTTP_400_BAD_REQUEST代替纯数字
from rest_framework import status
# REST框架提供两个装饰器装饰API视图
# --- @api_view 装饰器用于基于视图的方法上
# --- APIView类用于基于视图的类上，提供一些确保你的视图中接收Request对象等功能
from rest_framework.decorators import api_view, detail_route
# REST框架的Response响应对象，用于渲染内容和内容协商来绝对正确的内容类型并返回给客户端的模板响应(TemplateResponse)
from rest_framework.response import Response
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer, UserSerializer
# 第五版 使用基于视图的一般类(generic class)
from rest_framework import generics
# 为用户添加只读视图
from django.contrib.auth.models import User
# 为视图添加需要的权限
from rest_framework import permissions
from snippets.permissions import IsOwnerOrReadOnly
# 为我们的api根创建一个端点
from rest_framework.reverse import reverse
# 创建一个高亮的snippets端点
from rest_framework import renderers
# 使用视图集(ViewSets)重构
from rest_framework import viewsets

# 使默认路由DefaultRouter类会自动为我们创建api根视图 可以注掉以下方法
'''
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format) 
})'''




# 用SnippetHighlight视图类来代替SnippetList和SnippetDetail
class SnippetViewSet(viewsets.ModelViewSet):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    perimission_classes = (permissions.IsAuthenticatedOrReadOnly,
                           IsOwnerOrReadOnly,)

    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)
 
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

'''
class SnippetList(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    
    # 允许修改任何请求对象或请求连接的信息
 
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
'''

# 用UserViewSet替换UserList和UserDetail
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
'''
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
''' 
# 创建一个高亮的snippets端点 
class SnippetHighlight(generics.GenericAPIView):
    queryset = Snippet.objects.all()
    renderer_classes = (renderers.StaticHTMLRenderer,)

    def get(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)


# 第四版 使用mixins混合
#from rest_framework import mixins
#from rest_framework import generics 
# GenericAPIView基类提供核心功能  ListModelMixin和CreateModelMixin提供.list()和.create()动作，合适的动作绑定get和post方法
'''
class SnippetList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
'''   

'''
class SnippetDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Snippet.objects.all()
    seriailzer_class = SnippetSerializer
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

'''
# 用GenericAPIView类提供核心功能添加混合，来提供.retrieve()读，.update()和.destroy()动作


# 第三版 使用cbv
# cbv方式写api 基于视图的类
#from rest_framework.views import APIView
# snippet list   get和post
'''
class SnippetList(APIView):
    def get(self,request,format=None):
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippet, many=True)
        return Response(serializer.data) 

    def post(self, request, format=None):
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_404_BAD_REQUEST)


# snippet 详情 增删改查
'''
'''
class SnippetDetail(APIView):
    def get_object(self,pk):
        try:
            return Snippet.objects.get(pk=pk)
        except Snippet.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_404_BAD_REQUEST)

    def delete(self, reuqest, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
'''



'''
# 第二版
@api_view(['GET', 'POST'])
def snippet_list(request):
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # REST框架介绍了一个请求Request对象
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail(request, pk):
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_404_BAD_REQUEST)

    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
'''

'''
# 第一版
# 通过创建HttpResponse的一个子类，用这个子类渲染任何我们返回的json数据
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
# 视图避免跨站伪造请求 使用csrf_exempt,前端代码使用csrf_token
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
# Create your views here.

@csrf_exempt
def snippet_list(request):
    # 列出所有存在的snippet视图或者创建一个新的snippet对象
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        print(snippets)
        serializer = SnippetSerializer(snippets, many=True)
        print(serializer.data)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def snippet_detail(request, pk):
    # 读取，更新或者删除单个snippet对象的视图
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Sippet.DoesNotExist:
        return HttpResponse(status=404)
 
    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=204) 
'''
