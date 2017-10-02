from functions import OP_DICT


class Node(object):
    """Tree implemenation using multiple nodes

    Node of a tree that is itself a tree, as it contains two children.
    Contains a string that represents the tree contents and a height value,
    that stores the tree's height value.
    """
    def __init__(self, content, left=None, right=None):
        self.__left = left
        self.__right = right
        self.__content = content
        self.update()

    def __str__(self):
        return self._string

    def update(self):
        self._update_height()
        self._update_string()

    def _update_height(self):
        l_height = -1 if self.__left is None else self.__left.get_height()
        r_height = -1 if self.__right is None else self.__right.get_height()
        self.__height = max(l_height, r_height) + 1

    def get_height(self):
        return self.__height

    def set_content(self, content):
        self.__content = content

    def get_content(self):
        return self.__content

    def set_left_child(self, left_child):
        self.__left = left_child
        self.update()

    def set_right_child(self, right_child):
        self.__right = right_child
        self.update()

    def get_left_child(self):
        return self.__left

    def get_right_child(self):
        return self.__right


class TerminalNode(Node):
    """Leaf of a tree.

    TerminalNode extends Node to implement a leaf node. Its children
    store None.

    Extends:
        Node
    """
    def __init__(self, terminal):
        super(TerminalNode, self).__init__(terminal)

    def eval(self, var_map):
        content = self.get_content()
        return content if content not in var_map else var_map[content]

    def _update_string(self):
        self._string = str(self.get_content())


class FunctionNode(Node):
    """Node that contains a function.

    FunctionNode extends Node to implement a node that contains a function.
    This node cannot be a leaf.

    Extends:
        Node
    """
    def __init__(self, terminal, left, right):
        super(FunctionNode, self).__init__(terminal, left, right)

    def eval(self, var_map):
        left_child = self.get_left_child()
        right_child = self.get_right_child()
        content = self.get_content()

        left_eval = left_child.eval(var_map)

        if right_child is None:
            return content(left_eval)
        else:
            return content(left_eval, right_child.eval(var_map))

    def _update_string(self):
        """ Updates the string that represents the Node's tree """

        left_child = self.get_left_child()
        right_child = self.get_right_child()
        content = self.get_content()

        n = str(content) if content not in OP_DICT else OP_DICT[content]
        s = ''

        if right_child is None:
            s = n + ' ' + str(left_child)
        else:
            s = str(left_child) + ' ' + n + ' ' + str(right_child)

        self._string = '(' + s + ')'
