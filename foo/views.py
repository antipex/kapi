# from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from foo.models import Foo
from foo.serializers import FooSerializer


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
def foo_list(request):
    """
    List all foos or create a new foo.
    """

    if request.method == 'GET':
        foos = Foo.objects.all()
        serializer = FooSerializer(foos, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = FooSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)


@csrf_exempt
def foo_detail(request, pk):
    """
    Retrieve, update, or delete a foo.
    """
    try:
        foo = Foo.objects.get(pk=pk)
    except Foo.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = FooSerializer(foo)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = FooSerializer(foo, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        foo.delete()
        return HttpResponse(status=204)
