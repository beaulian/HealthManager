from scrapy.dupefilter import RFPDupeFilter


class SeenURLFilter(RFPDupeFilter):
    def __init__(self):
        self.urls_seen = set()
        RFPDupeFilter.__init__(self)

    def request_seen(self, request):
        if request.url in self.urls_seen:
            return True
        else:
            self.urls_seen.add(request.url)