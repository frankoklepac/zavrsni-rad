from django import template

register = template.Library()

@register.filter
def replace(value, arg):
    search, replace = arg.split(',')
    return value.replace(search, replace)
