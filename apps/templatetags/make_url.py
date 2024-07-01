from django.template import Library

register = Library()


@register.filter()
def make_url(request, page):
    pass
    # result = '?'
    # category_id = request.GET.get('category')
    # if category_id:
    #     result += f'category={category_id}&'
    # if page:
    #     result += f'page={page}'
    #
    # return result


