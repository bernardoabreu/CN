import math
import sys


if sys.version_info[0] < 3:
    MAXINT = sys.maxint
else:
    MAXINT = sys.maxsize


class Individual(object):
    def __init__(self, tree):
        self.root = tree
        self.error = None

    def get_error(self):
        return self.error

    def __eval(self, data):
            return (self.root.eval({('X' + str(i)): x
                    for i, x in enumerate(data[:-1])}) - (data[-1]))**2

    def eval(self, data_input, max_height=None):

        try:
            length = len(data_input)
            self.error = math.sqrt(sum(map(self.__eval, data_input)) / length)

            if max_height is not None and self.root.get_height() > max_height:
                self.error = 10000000 + self.error

            self.error = min(self.error, MAXINT)
        except OverflowError:
            self.error = MAXINT
        except Exception:
            self.error = MAXINT

        return self.error

    def __replace_node(self, node, old_node, new_node):
        """Auxiliar method of replace_node.

        Travels through the nodes of the tree recursively searching for the
        node to replace on each node's children. When the node is found, the
        children is replaced.

        Arguments:
            node {Node} -- Current node on the recursion
            old_node {Node} -- Node that is going to be replaced
            new_node {Node} -- New node to replace the old_node

        Returns:
            bool -- The node was successfully replaced
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
        """Replaces a node in the tree with a different node

        Calls __replace_node to replace any node that is not root. Otherwise,
        replaces whole tree.

        Arguments:
            old_node {Node} -- Node that is going to be replaced
            new_node {Node} -- New node to replace the old_node

        Returns:
            bool -- The node was successfully replaced
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
