class Point(object):
    def __init__(self, x, y, c, d):
        self.x = float(x)
        self.y = float(y)
        self.capacity = float(c)
        self.demand = float(d)

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_capacity(self):
        return self.capacity

    def get_demand(self):
        return self.demand
