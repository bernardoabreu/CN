class Point(object):
    def __init__(self, x, y, c, d):
        self.x = float(x)
        self.y = float(y)
        self.capacity = float(c)
        self.demand = float(d)
        self.current_capacity = self.capacity

    def reset_capacity(self):
        self.current_capacity = self.capacity

    def remove_capacity(self, cap):
        self.current_capacity -= cap

    def get_coord(self):
        return (self.x, self.y)

    def get_capacity(self):
        return self.current_capacity

    def get_demand(self):
        return self.demand
