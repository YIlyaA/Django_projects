from django.core.paginator import Paginator
from django.db.models import QuerySet


class PaginatedViewMixin:
    paginate_by = 5

    def paginate_queryset(self, queryset: QuerySet, page_size: int) -> QuerySet:
        paginator = Paginator(queryset, page_size)
        page_number = self.request.GET.get("page")
        return paginator.get_page(page_number)
