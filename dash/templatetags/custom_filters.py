from django import template

register = template.Library()

@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key)


# Strips whitespace and converts to lowercase.
@register.filter(name='normalize')
def normalize(value):
    if isinstance(value, str):
        return value.strip().lower()
    return value