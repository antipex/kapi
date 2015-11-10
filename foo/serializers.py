from rest_framework import serializers
from foo.models import Foo


class FooSerializer(serializers.ModelSerializer):
    class Meta:
        model = Foo
        fields = ('id', 'name', 'created')
