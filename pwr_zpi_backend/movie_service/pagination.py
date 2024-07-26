from rest_framework import pagination
from rest_framework.response import Response


class CustomPageNumberPagination(pagination.PageNumberPagination):
    page_size_query_param = 'perPage'

    def get_next_page_num(self):
        if not self.page.has_next():
            return None
        return self.page.next_page_number()

    def get_previous_page_num(self):
        if not self.page.has_previous():
            return None
        return self.page.previous_page_number()

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'next': self.get_next_page_num(),
            'previous': self.get_previous_page_num(),
            'results': data
        })
