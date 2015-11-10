# from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from foo.models import Foo
from foo.serializers import FooSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


class FooList(APIView):
    """
    List all foos or create a new foo.
    """
    def get(self, request, format=None):
        foos = Foo.objects.all()
        serializer = FooSerializer(foos, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = FooSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FooDetail(APIView):
    """
    Retrive, update, or delete a foo instance.
    """
    def get_object(self, pk):
        try:
            return Foo.objects.get(pk=pk)
        except Foo.DoesNotExist:
            raise Http404

        def get(self, request, pk, format=None):
            foo = self.get_object(pk)
            serializer = FooSerializer(foo)
            return Response(serializer.data)

        def put(self, request, pk, format=None):
            foo = self.get_object(pk)
            serializer = FooSerializer(foo, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)

        def delete(self, request, pk, format=None):
            foo = self.get_object(pk)
            foo.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
