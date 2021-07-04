class PagedContent():
    def __init__(self, page, data, total, page_size):
        self.page = page
        self.data = data
        self.total = total
        self.page_size = page_size