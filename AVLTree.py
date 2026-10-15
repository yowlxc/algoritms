import sys


class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    def __init__(self):
        self.root = None

    def height(self, node):
        return node.height if node else 0

    def balance_factor(self, node):
        return self.height(node.right) - self.height(node.left)

    def fix_height(self, node):
        node.height = 1 + max(
            self.height(node.left),
            self.height(node.right)
        )

    def rotate_right(self, a):
        b = a.left
        a.left = b.right
        b.right = a

        self.fix_height(a)
        self.fix_height(b)
        return b

    def rotate_left(self, a):
        b = a.right
        a.right = b.left
        b.left = a

        self.fix_height(a)
        self.fix_height(b)
        return b

    def balance(self, node):
        if node is None:
            return None

        self.fix_height(node)
        bf = self.balance_factor(node)

        if bf == 2:
            if self.balance_factor(node.right) < 0:
                node.right = self.rotate_right(node.right)
            return self.rotate_left(node)

        if bf == -2:
            if self.balance_factor(node.left) > 0:
                node.left = self.rotate_left(node.left)
            return self.rotate_right(node)

        return node

    def add(self, key):
        self.root = self._add(self.root, key)

    def _add(self, node, key):
        if node is None:
            return Node(key)

        if key < node.key:
            node.left = self._add(node.left, key)
        elif key > node.key:
            node.right = self._add(node.right, key)
        else:
            return node

        return self.balance(node)

    def find_min(self, node):
        while node.left is not None:
            node = node.left
        return node

    def remove_min(self, node):
        if node.left is None:
            return node.right

        node.left = self.remove_min(node.left)
        return self.balance(node)

    def delete(self, key):
        self.root = self._delete(self.root, key)

    def _delete(self, node, key):
        if node is None:
            return None

        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            left = node.left
            right = node.right

            if right is None:
                return left

            min_node = self.find_min(right)
            min_node.right = self.remove_min(right)
            min_node.left = left
            return self.balance(min_node)

        return self.balance(node)

    def exists(self, key):
        node = self.root

        while node is not None:
            if key == node.key:
                return True
            if key < node.key:
                node = node.left
            else:
                node = node.right

        return False

    def next_key(self, key):
        node = self.root
        candidate = None

        while node is not None:
            if node.key >= key:
                candidate = node.key
                node = node.left
            else:
                node = node.right

        return candidate

    def prev_key(self, key):
        node = self.root
        candidate = None

        while node is not None:
            if node.key <= key:
                candidate = node.key
                node = node.right
            else:
                node = node.left

        return candidate

    def get_root(self):
        if self.root is None:
            return "Empty"
        return str(self.root.key)

    def get_height(self):
        return str(self.height(self.root))

    def print_tree(self):
        if self.root is None:
            return "Empty"

        result = []
        stack = [self.root]

        while stack:
            node = stack.pop()
            result.append(str(node.key))

            if node.right is not None:
                stack.append(node.right)
            if node.left is not None:
                stack.append(node.left)

        return " ".join(result)


def main():
    input = sys.stdin.readline
    q = int(input())
    tree = AVLTree()
    output = []

    for i in range(q):
        command = input().split()
        operation = command[0]

        if operation == "add":
            tree.add(int(command[1]))

        elif operation == "del":
            tree.delete(int(command[1]))

        elif operation == "exists":
            output.append(
                "YES" if tree.exists(int(command[1])) else "NO"
            )

        elif operation == "next":
            result = tree.next_key(int(command[1]))
            output.append(str(result) if result is not None else "None")

        elif operation == "prev":
            result = tree.prev_key(int(command[1]))
            output.append(str(result) if result is not None else "None")

        elif operation == "root":
            output.append(tree.get_root())

        elif operation == "height":
            output.append(tree.get_height())

        elif operation == "print":
            output.append(tree.print_tree())

    sys.stdout.write("\n".join(output))


if __name__ == "__main__":
    main()
