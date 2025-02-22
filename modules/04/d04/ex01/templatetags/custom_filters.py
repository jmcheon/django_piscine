from django import template

register = template.Library()


@register.filter
def escape_braces(value):
    return value.replace("{", "&#123;").replace("}", "&#125;")
