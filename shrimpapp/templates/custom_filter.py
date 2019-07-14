from django import template

register = template.Library()

@register.filter(name='splitFirst')
def splitFirst(value, key):
    #print("-----****" + str(value.split(key)[0]))
    return int(value.split(key)[0])

@register.filter(name='splitSecond')
def splitSecond(value, key):
    #print("-----****" + str(value.split(key)[1]))
    return value.split(key)[1]