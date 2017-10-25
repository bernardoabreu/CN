class Group(object):
    def __init__(self):
        self.median = None
        self.points = set()
        self.total_distance = 0.0

    def add_median(self, point):
        self.median = point

    def add_point(self, point):
        self.points.add(point)

    def get_median(self):
        return self.median

    def get_points(self):
        return list(self.points)

    def __contains__(self, key):
        return key in self.points

    def eval(self):
        return
