from rest_framework import serializers
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES
# 将用户添加到api
from django.contrib.auth.models import User


# 序列化类(serializer class)定义了一些需要被序列化/反序列化字段。
# create()与update()方法定义在调用serializer.save()时成熟的实例是如何被创建和修改的。
# 使用超链快速重写现存的序列
class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight', format='html')

    class Meta:
        # 元数据指定要序列化的模型和字段
        model = Snippet
        fields = ('url', 'id', 'highlight', 'owner', 'title', 'code', 'linenos', 'language', 'style')

class UserSerializer(serializers.HyperlinkedModelSerializer):
    snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail', read_only=True)
    
    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'snippets')

'''
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    code = serializers.CharField(style={'base_template':'textarea.html'})
    linenos = serializers.BooleanField(required=False)
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
    style = serializers.ChoiceField(choices=STYLE_CHOICES, default='firendly')
    
    def create(self, validated_data):
        # 创建并返回一个新的Snippet实例，给出有效数据
        return Snippet.objects.create(**validated_data)
   
    def update(self, instance, validated_data):
        # 更新并返回一个存在的Snippet实例，给出有效数据
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = valiated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance
'''
