class Point(object):
    def __init__(self, x, y, c, d):
        self.x = float(x)
        self.y = float(y)
        self.__capacity = float(c)
        self.__demand = float(d)

    def get_coord(self):
        return (self.x, self.y)

    def get_capacity(self):
        return self.__capacity

    def get_demand(self):
        return self.__demand
