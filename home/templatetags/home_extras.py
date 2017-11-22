from django import template

register = template.Library()

@register.filter(name='joinby')
def joinby(value, arg):
    return arg.join(value)
	
def key(d, key_name):
    return d[key_name]
key = register.filter('key', key)
#Usage: {{ dict|key:key_name }}