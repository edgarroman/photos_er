from django import template

register = template.Library()

FILTER_SEPARATOR = '|'

def its(value,arg):
    '''
    This filter takes a url and appends the appropriate prefix and
    transformation to route this request through its

    The argument should be in a form of:
    "<namespace>|<transform>"

    Where <namespace> is the ITS namespace to utilize
    And <transform> is the ITS image transform requested

    Example:
    {% load its %}
    <img src="{{ image_url|its:"demo|.resize.200x200.jpg" }}">

    '''
    namespace,sep,transform = arg.partition(FILTER_SEPARATOR)
    if not sep:
        return value

    url_stub = value.replace('/media/','')

    final_url = 'http://image.pbs.org/%s/%s%s' % (namespace, url_stub, transform)

    return final_url

register.filter('its',its)
