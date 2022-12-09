from django import template
from django.http import QueryDict

register = template.Library()
@register.filter(name='lookup')
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter(name='getlist')
def getlist(query_dict: QueryDict, key):
    return query_dict.getlist(key)