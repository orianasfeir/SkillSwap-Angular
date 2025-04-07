from django import template

register = template.Library()

@register.filter
def divide_by_two(value):
    try:
        return int(value) // 2
    except (ValueError, TypeError):
        return 0 