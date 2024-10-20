from server.util.util import str_to_int, ValidationUtils


class Filter:
    def __init__(self, form_data):
        self.page = str_to_int(form_data.get('page'), 0)
        self.limit = str_to_int(form_data.get('limit'), 0)
        self.order_by = form_data.get('order')
        self.order_by_desc = form_data.get('desc')

    def get_order_by_sql(self) -> str:
        if ValidationUtils.is_empty(self.order_by):
            return ""
        return f" ORDER BY {self.order_by} {self.order_by_desc}"

    def get_limit_sql(self) -> str:
        if self.page < 1 or self.limit < 1:
            return ""
        return f" LIMIT {self.limit} OFFSET {(self.page - 1) * self.limit}"
