from rest_framework.pagination import PageNumberPagination


class LimitPageNumberPagination(PageNumberPagination):
    '''
    Класс пагинатора. Количество объектов на странице можно задавать 
    с помощью параметра limit и страницу с помощью параметра page.
    '''
    page_size_query_param = 'limit'
