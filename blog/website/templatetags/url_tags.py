from django.utils.http import urlencode
from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def change_params(context, **kwargs):
    query = context["request"].GET.dict()
    query.update(kwargs)
    return urlencode(query)

@register.filter
def break_long_words(value, max_length=20):
    words = value.split()
    for i in range(len(words)):
        if len(words[i]) > max_length:
            words[i] = ' '.join([words[i][j:j + max_length] for j in range(0, len(words[i]), max_length)])
    return ' '.join(words)