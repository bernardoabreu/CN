import math
import sys


class Individual(object):
    """[summary]

    [description]
    """
    def __init__(self, tree):
        self.root = tree
        self.error = None

    def get_error(self):
        return self.error

    def __eval(self, data):
        return (self.root.eval({('X' + str(i)): x
                for i, x in enumerate(data[:-1])}) - (data[-1]))**2

    def eval(self, data_input, max_height=None):

        if max_height is not None and self.root.get_height() > max_height:
            self.error = sys.maxint
        else:
            length = len(data_input)
            self.error = math.sqrt(sum(map(self.__eval, data_input)) / length)

        return self.error

    def __replace_node(self, node, old_node, new_node):
        """[summary]

        [description]

        Arguments:
            node {[type]} -- [description]
            old_node {[type]} -- [description]
            new_node {[type]} -- [description]

        Returns:
            bool -- [description]
        """
        if node is None:
            return False

        node_left = node.get_left_child()
        node_right = node.get_right_child()

        if node_left == old_node:
            node.set_left_child(new_node)
            return True

        if node_right == old_node:
            node.set_right_child(new_node)
            return True

        if self.__replace_node(node_left, old_node, new_node):
            node.update()
            return True
        else:
            right_result = self.__replace_node(node_right, old_node, new_node)
            node.update()
            return right_result

    def replace_node(self, old_node, new_node):
        """[summary]

        [description]

        Arguments:
            old_node {[type]} -- [description]
            new_node {[type]} -- [description]

        Returns:
            bool -- [description]
        """
        if self.root == old_node:
            self.root = new_node
            return True
        else:
            result = self.__replace_node(self.root, old_node, new_node)
            self.root.update()
            return result

    def __get_list(self, node, node_list):
        if node is None:
            return

        left = node.get_left_child()
        right = node.get_right_child()

        self.__get_list(left, node_list)
        node_list.append(node)
        self.__get_list(right, node_list)

    def get_list(self):
        node_list = []
        self.__get_list(self.root, node_list)

        return node_list

    def __str__(self):
        return str(self.root)
