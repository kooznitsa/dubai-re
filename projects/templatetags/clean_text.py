from django import template

register = template.Library()

replace_dict = {'"': '', ',': ' | ', '{': '', '}': ''}

@register.filter
def clean_text(text):
    for old, new in replace_dict.items():
        text = text.replace(old, new)
    return text