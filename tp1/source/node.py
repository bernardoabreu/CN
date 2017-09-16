from functions import OP_DICT


class Node(object):
    def __init__(self, content, left=None, right=None):
        self.__left = left
        self.__right = right
        self.__content = content
        self.update_height()

    def __str__(self):
        return str(self.__content)

    def update_height(self):
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
        self.update_height()

    def set_right_child(self, right_child):
        self.__right = right_child
        self.update_height()

    def get_left_child(self):
        return self.__left

    def get_right_child(self):
        return self.__right

    def print_tree(self):
        self.__print(self)
        print

    def __print(self, node, level=0):
        if node is None:
            return

        left_child = node.get_left_child()
        right_child = node.get_right_child()
        content = node.get_content()

        n = str(node) if content not in OP_DICT else OP_DICT[content]

        # print ' ' * level, n + '[' + str(node.get_height()) + ']'
        if right_child is None:
            print n,  # + '[' + str(node.get_height()) + ']',

        if left_child is not None:
            print '(',
            self.__print(left_child, level + 1)
            if right_child is None:
                print ')',

        if right_child is not None:
            print n,  # + '[' + str(node.get_height()) + ']',
            self.__print(right_child, level + 1)

            print ')',


class Terminal_Node(Node):
    def __init__(self, terminal):
        super(Terminal_Node, self).__init__(terminal)

    def eval(self, var_map):
        content = self.get_content()
        return content if content not in var_map else var_map[content]


class Function_Node(Node):

    def __init__(self, terminal, left, right):
        super(Function_Node, self).__init__(terminal, left, right)

    def eval(self, var_map):
        left_child = self.get_left_child()
        right_child = self.get_right_child()
        content = self.get_content()

        left_eval = left_child.eval(var_map)

        if right_child is None:
            return content(left_eval)
        else:
            return content(left_eval, right_child.eval(var_map))
