import os
from django import template

register = template.Library()

@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key)




@register.filter
def basename(value):
    return os.path.basename(value.name)


@register.filter(name='get_grade')
def get_grade(value, arg):
    """Retrieve value from the dictionary using a variable key."""
    return value.get(arg, 'No grade')