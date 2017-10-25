class Group(object):
    def __init__(self):
        self.median = None
        self.points = set()
        self.total_distance = 0.0

    def add_point(self, point):
        if self.median is None:
            self.median = point
        else:
            self.points.add(point)

    def get_median(self):
        return self.median

    def __contains__(self, key):
        return key in self.points

    def add_distance(self, dist):
        self.total_distance += dist

    def get_distance(self):
        return self.total_distance
