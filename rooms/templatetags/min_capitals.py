from atexit import register
from django import template

register = template.Library()

@register.filter
def min_capitals(value):
    return value.capitalize()