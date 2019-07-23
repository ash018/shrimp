from django import template
import re

register = template.Library()

@register.filter(name='colorCheck')
def colorCheck(value):
    col = 'btn-info'
    pkgMat = re.split('-',str(value))
    for i in pkgMat:
        col = ''
        k = re.split('!',str(i))
        if k[0] != '1':
            col = 'add-pkg-item'
            break
        else:
            col = 'btn-info'
            break

    return str(col)


@register.filter(name='splitFirst')
def splitFirst(value, key):
    #print("-----****" + str(value.split(key)[0]))
    return int(value.split(key)[0])


@register.filter(name='splitSecond')
def splitSecond(value, key):
    #print("-----****" + str(value.split(key)[1]))
    return value.split(key)[1]