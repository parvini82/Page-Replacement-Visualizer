class PageReplacement:
    def __init__(self, frame_size):
        self.frame_size = frame_size
        self.frames = []
        self.page_faults = 0

    def fifo(self, pages):
        self.page_faults = 0
        self.frames = []

        for page in pages:
            if page not in self.frames:
                if len(self.frames) < self.frame_size:
                    self.frames.append(page)
                else:
                    self.frames.pop(0)
                    self.frames.append(page)
                self.page_faults += 1
        return self.page_faults
    def lru(self, pages):
        self.page_faults = 0
        self.frames = []
        recent_pages = []

        for page in pages:
            if page not in self.frames:
                if len(self.frames) < self.frame_size:
                    self.frames.append(page)
                else:
                    lru_page = recent_pages.pop(0)
                    self.frames.remove(lru_page)
                    self.frames.append(page)
                self.page_faults += 1
            else:
                recent_pages.remove(page)
            recent_pages.append(page)
        return self.page_faults


def optimal_page_replacement(pages, frame_size):
    frames = []
    page_faults = 0

    for i, page in enumerate(pages):
        if page not in frames:
            if len(frames) < frame_size:
                frames.append(page)
            else:
                # پیدا کردن صفحه‌ای که در آینده دورتر نیاز است
                future_uses = []
                for frame in frames:
                    if frame not in pages[i + 1:]:
                        future_uses.append(float('inf'))  # اگر صفحه دیگر استفاده نشود
                    else:
                        future_uses.append(pages[i + 1:].index(frame))
                # جایگزین کردن صفحه‌ای که دورترین استفاده را دارد
                farthest_page = frames[future_uses.index(max(future_uses))]
                frames[frames.index(farthest_page)] = page
            page_faults += 1
    return page_faults
