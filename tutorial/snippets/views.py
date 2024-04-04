from django.shortcuts import render

from django.http import HttpResponse,JsonResponse

from django.views.decorators.csrf import csrf_exempt

from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,permissions
from rest_framework import generics
from rest_framework import mixins
from django.http import Http404

from snippets.models import Snippet

from django.contrib.auth.models import User
from snippets.serializers import SnippetSerializers,UserSerializer

from django.contrib.auth.models import User
from snippets.permissions import IsOwnerOrReadOnly


# @api_view(['GET','POST'])
# def snippet_list(request,format=None):
#     """
#     list all snippets

#     """
#     if request.method=='GET':
#         snippets = Snippet.objects.all()
#         serializer= SnippetSerializers(snippets, many=True)
#         return JsonResponse({"data":serializer.data},safe=False)
#     elif request.method=='POST':
#         data= JSONParser().parse(request)
#         serializer= SnippetSerializers(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
#         return JsonResponse(serializer.errors,status=status.HTTP_404_NOT_FOUND)
    

# @api_view(['GET','PUT','DELETE'])
# def snippet_detail(request, pk,format=None):
#     """ 
#     retrive, update, delete

#     """

#     try:
#         snippet=Snippet.objects.get(pk=pk)
#     except Snippet.DoesNotExist:
#         return HttpResponse(status=status.HTTP_404_NOT_FOUND)

#     if request.method=='GET':

#         serializer=SnippetSerializers(snippet)

#         return JsonResponse({"data":serializer.data})
#     elif request.method=='PUT':
#         data=JSONParser().parse(request)

#         serializer=SnippetSerializers(snippet,data=data)

#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data,status=status.HTTP_202_ACCEPTED)
#         return JsonResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
#     elif request.method=='DELETE':
#         snippet.delete()
#         return HttpResponse(status=status.HTTP_204_NO_CONTENT)

# class SnippetList(APIView):
#     """
#     Get  all snippets and create  new snippet

#     """
#     def get(self, request, format=None):
#         snippet=Snippet.objects.all()

#         serializer = SnippetSerializers(snippet, many=True)
#         return Response(serializer.data)
    
#     def post(self, request, format=None):
#         serializer=SnippetSerializers(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_201_CREATED)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
# class SnippetDetails(APIView):
#     """
#     Get one snippet andupdate one and delete one
#     """
#     def get_object(self,pk):

#         try:
#             return Snippet.objects.get(pk=pk)
#         except Snippet.DoesNotExist:
#             return Http404
        
#     def get(self,request,pk,format=None):
#         snippet=self.get_object(pk)
#         serializer=SnippetSerializers(snippet)
#         return Response(serializer.data)
    
#     def put(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         serializer=SnippetSerializers(snippet,data=request.data)

#         if serializer.is_valid():

#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def delete(self, request, pk):

#         snippet=self.get_object(pk)

#         snippet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

##using mixins

class SnippetList(
                mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset=Snippet.objects.all()
    permission_classes=[permissions.IsAuthenticatedOrReadOnly]
    serializer_class=SnippetSerializers

    def get(self, request, *args,**kwargs):

        return self.list(request, *args,**kwargs)
    
    def post(self, request, *args, **kwargs):

        return self.create(request,*args,**kwargs)
    
    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)
    

class SnippetDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                      IsOwnerOrReadOnly]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
class UserList(generics.ListAPIView):
    queryset=User.objects.all()
    serializer_class=UserSerializer

class UserDetail(generics.RetrieveAPIView):

    queryset=User.objects.all()
    serializer_class=UserSerializer

    









        






