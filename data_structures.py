'''
    Basic datastructures
    Was forced to use doctest. Without mocking and a non inline test framework,
    the tests look a bit messy and tedious.
    @author Bailey Ammons
'''


class SinglyLinkedNode(object):

    def __init__(self, item=None, next_link=None):
        super(SinglyLinkedNode, self).__init__()
        self._item = item
        self._next = next_link

    @property
    def item(self):
        return self._item

    @item.setter
    def item(self, item):
        self._item = item

    @property
    def next(self):
        return self._next

    @next.setter
    def next(self, next):
        self._next = next

    def __repr__(self):
        return repr(self.item)


class SinglyLinkedList(object):

    def __init__(self):
        super(SinglyLinkedList, self).__init__()
        self._head = None
        self._current = None

    def __len__(self):
        ''' Get the length of the linked list
        >>> obj = generateLinkedList()
        >>> len(obj)
        100
        '''
        count = 0
        node = self._head
        while(node is not None):
            count += 1
            node = node.next
        return count

    def __iter__(self):
        self._current = self._head
        while self._current is not None:
            yield self._current
            self._current = self._current.next

    def __contains__(self, item):
        ''' finds out if element exists within the collection
        >>> obj = generateLinkedList()
        >>> 4004 in obj
        True
        >>> 101 in obj
        False
        '''
        found = False
        self._current = self._head
        while found is False and self._current is not None:
            if self._current.item[0] == item:
                found = True
            else:
                self._current = self._current.next

        return found

    def remove(self, item):
        ''' Remove element from collection based using item
        >>> obj = generateLinkedList()
        >>> obj.remove(4004)
        >>> 4004 in obj
        False
        '''
        for n in self:
            # when you're at the head of the list
            if n.item[0] == item:
                n = n.next
                self._head = n

            if n.next is not None and n.next.item[0] == item:
                n.next = n.next.next

    def prepend(self, item):
        ''' add element to the head of the collection
        >>> obj = generateLinkedList()
        >>> obj.prepend((1001, 1001))
        >>> obj._head.item
        (1001, 1001)
        '''
        self._head = SinglyLinkedNode(item, self._head)
        self._current = self._head

    def __repr__(self):
        '''
        iterate through and print list
        '''
        s = "List:" + "->".join([
            "(" + str(i.item[0]) + ", " + str(i.item[1]) + ")" for i in self])
        return s


class ChainedHashDict(object):

    def __init__(self, bin_count=10, max_load=0.7, hashfunc=hash):
        super(ChainedHashDict, self).__init__()

        self._bin_count = bin_count
        self._bins_used = 0
        self._max_load = max_load
        self._hashfunc = hashfunc
        self._chd = [SinglyLinkedList() for i in range(0, self.bin_count)]

    @property
    def load_factor(self):
        ''' return the load factor of the table
        >>> obj = generateChainHashTest()
        >>> obj.load_factor
        0.725
        '''
        return float(self.bins_used) / float(self.bin_count)

    @property
    def bins_used(self):
        ''' return the number of bins used in the table
        >>> obj = generateChainHashTest()
        >>> obj.bins_used
        58
        '''
        return self._bins_used

    @bins_used.setter
    def bins_used(self, bins):
        self._bins_used = bins

    @property
    def bin_count(self):
        ''' return the number of bins in the table
        >>> obj = generateChainHashTest()
        >>> obj.bin_count
        80
        '''
        return self._bin_count

    @bin_count.setter
    def bin_count(self, bc):
        self._bin_count = bc

    def rebuild(self, bincount):
        ''' rebuilds the table when it exceeds the max load
        test to see if all keys are still in the table after a few rebuilds
        >>> obj = generateChainHashTest()
        >>> for i in test_keys:
        ...     i in obj
        ...
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        '''
        # Rebuild this hash table with a new bin count
        self.bin_count = bincount
        self.bins_used = 0
        temp = self._chd
        self._chd = [SinglyLinkedList() for i in range(0, self.bin_count)]
        for t in temp:
            for n in t:
                index = self._hashfunc(n.item[0]) % self.bin_count
                self[n.item[0]] = n.item[1]

    def __getitem__(self, key):
        ''' get an item from the table
        use: node = table[key]
        >>> obj = generateChainHashTest()
        >>> node = obj[4004]
        >>> node.item
        (4004, 44)
        '''
        index = self._hashfunc(key) % self.bin_count
        list = self._chd[index]
        for n in list:
            if n.item[0] == key:
                return n
        return None

    def __setitem__(self, key, value):
        ''' set a node in table
        use: table[key] = value
        >>> obj = generateChainHashTest()
        >>> obj[101] = 100
        >>> 101 in obj
        True
        >>> node = obj[101]
        >>> node.item
        (101, 100)
        '''
        if self.load_factor > self._max_load:
            self.rebuild(self.bin_count * 2)

        index = self._hashfunc(key) % self.bin_count
        list = self._chd[index]
        for node in list:
            if node.item[0] == key:
                node.item = (key, value)
                return

        if list._head is None:
            self.bins_used = self.bins_used + 1
        item = (key, value)
        list.prepend(item)

    def __delitem__(self, key):
        ''' remove node from table
        use: del(table[key])
        >>> obj = generateChainHashTest()
        >>> 4004 in obj
        True
        >>> del(obj[4004])
        >>> 4004 in obj
        False
        '''
        list = self._chd[(self._hashfunc(key) % self.bin_count)]
        list.remove(key)
        if list._head is None:
            self.bins_used = self.bins_used - 1

    def __contains__(self, key):
        ''' if the node is in the table return true otherwise false
        use: key in table
        >>> obj = generateChainHashTest()
        >>> 4404 in obj
        True
        >>> 2180 in obj
        True
        >>> 3121 in obj
        False
        '''
        list = self._chd[(self._hashfunc(key) % self.bin_count)]
        return key in list

    def __len__(self):
        ''' returns the number of occupied bins
        use: len(table)
        >>> obj = generateChainHashTest()
        >>> len(obj)
        58
        '''
        return self.bins_used

    def display(self):
        ''' displays the bins and linked list within them
        >>> obj = generateChainHashTest()
        >>> obj.display()
        List:(8000, 16)
        List:
        List:(482, 11)
        List:(2243, 31)
        List:(8644, 87)->(4004, 44)->(4404, 67)
        List:
        List:(6, 19)->(5686, 60)
        List:(1847, 89)
        List:(8728, 13)
        List:(6649, 52)
        List:(8170, 26)
        List:
        List:(8332, 14)->(2492, 58)->(2972, 71)
        List:
        List:(6814, 0)->(8974, 21)->(8734, 47)
        List:(4255, 82)
        List:
        List:(1297, 99)->(2657, 32)
        List:
        List:(4739, 23)->(5299, 59)
        List:(2180, 75)->(7220, 22)
        List:(901, 73)
        List:(3302, 4)
        List:
        List:(4504, 30)->(8904, 15)
        List:(9865, 76)->(5545, 34)
        List:(1546, 41)
        List:(8987, 95)
        List:(3228, 10)->(28, 72)
        List:
        List:(9390, 33)->(590, 5)->(6270, 66)
        List:(7951, 63)->(31, 64)
        List:
        List:(5953, 48)
        List:
        List:(4515, 29)->(5795, 9)
        List:
        List:(4437, 78)->(1317, 17)->(9397, 53)
        List:(8998, 39)
        List:(3399, 37)
        List:(8600, 36)
        List:(5961, 94)->(8441, 8)
        List:(3962, 49)->(5002, 57)->(682, 65)->(282, 70)
        List:(1643, 80)
        List:(1244, 77)->(1004, 68)
        List:
        List:(846, 20)->(2286, 46)->(3246, 50)
        List:(2207, 96)
        List:
        List:(4529, 79)->(2529, 51)->(8049, 55)
        List:(5410, 2)
        List:(2211, 97)
        List:(2132, 90)->(6532, 56)
        List:(533, 38)
        List:(3494, 91)->(3334, 7)
        List:(2935, 84)->(4055, 69)
        List:(2376, 27)->(6456, 6)->(1256, 61)
        List:(9177, 1)
        List:(7498, 93)->(5978, 35)->(2298, 42)
        List:(9019, 98)->(6699, 81)->(5499, 40)->(619, 43)
        List:
        List:
        List:(3982, 54)
        List:(7583, 88)->(9983, 62)
        List:
        List:(5745, 3)
        List:(3666, 25)
        List:
        List:(7748, 92)
        List:
        List:(5510, 28)->(2230, 18)
        List:(3191, 74)->(2231, 45)
        List:
        List:
        List:
        List:
        List:(7196, 85)->(4316, 12)
        List:(5517, 83)
        List:(4078, 24)
        List:(2639, 86)
        '''
        for i in self._chd:
            print i


class OpenAddressHashDict(object):

    def __init__(self, bin_count=10, max_load=0.7, hashfunc=hash):
        super(OpenAddressHashDict, self).__init__()
        self._bin_count = bin_count
        self._max_load = max_load
        self._hashfunc = hashfunc
        self._bins_used = 0
        self._oahd = [None for i in range(0, self.bin_count)]

    @property
    def load_factor(self):
        ''' return the load factor of the table
        >>> obj = generateOpenHash()
        >>> obj.load_factor
        0.625
        '''
        return float(self.bins_used) / float(self.bin_count)

    @property
    def bin_count(self):
        ''' return the number of bins being in the table
        >>> obj = generateOpenHash()
        >>> obj.bin_count
        160
        '''
        return self._bin_count

    @bin_count.setter
    def bin_count(self, bc):
        self._bin_count = bc

    @property
    def bins_used(self):
        ''' returns the number of bins being used
        >>> obj = generateOpenHash()
        >>> obj.bins_used
        100
        '''
        return self._bins_used

    @bins_used.setter
    def bins_used(self, bins):
        self._bins_used = bins

    def rebuild(self, bincount):
        ''' rebuild the table when the load factor exceeds max load
        >>> obj = generateOpenHash()
        >>> for i in test_keys:
        ...     i in obj
        ...
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        '''
        temp = self._oahd
        self.bins_used = 0
        self.bin_count = bincount
        self._oahd = [None for i in range(0, self.bin_count)]

        for i in temp:
            if i is not None and i != 'DELETED':
                self[i[0]] = i[1]

    def __getitem__(self, key):
        ''' get an item from the list given the key
        use: value = table[key]
        >>> obj = generateOpenHash()
        >>> value = obj[2180]
        >>> value
        75
        '''
        i = 0
        index = (self._hashfunc(key) % self.bin_count)
        while(i < self.bin_count):
            val = self._oahd[(index + i) % self.bin_count]
            if val is None:
                return
            elif val[0] == key:
                return val[1]
            elif val == 'DELETED':
                return val
            else:
                i = i + 1

    def __setitem__(self, key, value):
        ''' pass set item in table using key and value
        use: table[key] = value
        >>> obj = generateOpenHash()
        >>> obj[101] = 1001
        >>> 101 in obj
        True
        >>> print(obj[101])
        1001
        '''
        if self.load_factor > self._max_load:
            self.rebuild(self.bin_count * 2)

        i = 0
        index = (self._hashfunc(key) % self.bin_count)
        while(i < self.bin_count):
            new_index = (index + i) % self.bin_count
            if self._oahd[new_index] is None:
                self.bins_used = self.bins_used + 1
                self._oahd[new_index] = (key, value)
                return
            elif self._oahd[new_index][0] == key:
                self._oahd[new_index] = (key, value)
                return
            else:
                i += 1

    def __delitem__(self, key):
        ''' Delete an item in the table
        use: del(table[key])
        >>> obj = generateOpenHash()
        >>> print(obj[1643])
        80
        >>> del(obj[1643])
        >>> print(obj[1643])
        DELETED
        '''
        i = 0
        index = self._hashfunc(key) % self.bin_count
        while(i < self.bin_count):
            val = self._oahd[(index + i) % self.bin_count]
            if val[0] == key:
                self._oahd[(index + i) % self.bin_count] = 'DELETED'
                return
            else:
                i += 1

    def __contains__(self, key):
        ''' returns whether or not the key exists in the collection
        use: key in table
        >>> obj = generateOpenHash()
        >>> 3494 in obj
        True
        >>> 100292 in obj
        False
        '''
        i = 0
        index = self._hashfunc(key) % self.bin_count
        while(i < self.bin_count):
            new_index = (index + i) % self.bin_count
            val = self._oahd[new_index]
            if val is not None and val != 'DELETED':
                if val[0] == key:
                    return True
            i = i + 1
        return False

    def __len__(self):
        '''return the number of bins occupied in the table
        >>> obj = generateOpenHash()
        >>> len(obj)
        100
        '''
        return self.bins_used

    def display(self):
        ''' Display the table
        >>> obj = generateOpenHash()
        >>> obj.display()
        bin 0: (8000, 16)
        bin 1: None
        bin 2: (482, 11)
        bin 3: (2243, 31)
        bin 4: (4004, 44)
        bin 5: (8644, 87)
        bin 6: (6, 19)
        bin 7: None
        bin 8: None
        bin 9: None
        bin 10: (8170, 26)
        bin 11: None
        bin 12: (8332, 14)
        bin 13: None
        bin 14: (8974, 21)
        bin 15: None
        bin 16: None
        bin 17: (1297, 99)
        bin 18: None
        bin 19: (5299, 59)
        bin 20: (7220, 22)
        bin 21: None
        bin 22: None
        bin 23: None
        bin 24: (4504, 30)
        bin 25: None
        bin 26: None
        bin 27: (8987, 95)
        bin 28: (3228, 10)
        bin 29: (28, 72)
        bin 30: (6270, 66)
        bin 31: (31, 64)
        bin 32: None
        bin 33: (5953, 48)
        bin 34: None
        bin 35: (5795, 9)
        bin 36: (4515, 29)
        bin 37: (1317, 17)
        bin 38: (8998, 39)
        bin 39: (3399, 37)
        bin 40: None
        bin 41: (5961, 94)
        bin 42: (5002, 57)
        bin 43: (682, 65)
        bin 44: (1004, 68)
        bin 45: (1643, 80)
        bin 46: (846, 20)
        bin 47: (2286, 46)
        bin 48: (3246, 50)
        bin 49: (8049, 55)
        bin 50: (4529, 79)
        bin 51: None
        bin 52: (2132, 90)
        bin 53: (533, 38)
        bin 54: None
        bin 55: (4055, 69)
        bin 56: (6456, 6)
        bin 57: (9177, 1)
        bin 58: (5978, 35)
        bin 59: (5499, 40)
        bin 60: (2298, 42)
        bin 61: (2935, 84)
        bin 62: (9019, 98)
        bin 63: (9983, 62)
        bin 64: (7583, 88)
        bin 65: None
        bin 66: None
        bin 67: None
        bin 68: (7748, 92)
        bin 69: None
        bin 70: (5510, 28)
        bin 71: None
        bin 72: None
        bin 73: None
        bin 74: None
        bin 75: None
        bin 76: None
        bin 77: (5517, 83)
        bin 78: (4078, 24)
        bin 79: (2639, 86)
        bin 80: None
        bin 81: None
        bin 82: None
        bin 83: None
        bin 84: (4404, 67)
        bin 85: None
        bin 86: (5686, 60)
        bin 87: (1847, 89)
        bin 88: (8728, 13)
        bin 89: (6649, 52)
        bin 90: None
        bin 91: None
        bin 92: (2492, 58)
        bin 93: (2972, 71)
        bin 94: (6814, 0)
        bin 95: (8734, 47)
        bin 96: (4255, 82)
        bin 97: (2657, 32)
        bin 98: None
        bin 99: (4739, 23)
        bin 100: (2180, 75)
        bin 101: (901, 73)
        bin 102: (3302, 4)
        bin 103: None
        bin 104: (8904, 15)
        bin 105: (5545, 34)
        bin 106: (1546, 41)
        bin 107: (9865, 76)
        bin 108: None
        bin 109: None
        bin 110: (590, 5)
        bin 111: (9390, 33)
        bin 112: (7951, 63)
        bin 113: None
        bin 114: None
        bin 115: None
        bin 116: None
        bin 117: (9397, 53)
        bin 118: (4437, 78)
        bin 119: None
        bin 120: (8600, 36)
        bin 121: (8441, 8)
        bin 122: (3962, 49)
        bin 123: (282, 70)
        bin 124: (1244, 77)
        bin 125: None
        bin 126: None
        bin 127: (2207, 96)
        bin 128: None
        bin 129: (2529, 51)
        bin 130: (5410, 2)
        bin 131: (2211, 97)
        bin 132: (6532, 56)
        bin 133: None
        bin 134: (3334, 7)
        bin 135: (3494, 91)
        bin 136: (2376, 27)
        bin 137: (1256, 61)
        bin 138: (7498, 93)
        bin 139: (619, 43)
        bin 140: (6699, 81)
        bin 141: None
        bin 142: (3982, 54)
        bin 143: None
        bin 144: None
        bin 145: (5745, 3)
        bin 146: (3666, 25)
        bin 147: None
        bin 148: None
        bin 149: None
        bin 150: (2230, 18)
        bin 151: (2231, 45)
        bin 152: (3191, 74)
        bin 153: None
        bin 154: None
        bin 155: None
        bin 156: (4316, 12)
        bin 157: (7196, 85)
        bin 158: None
        bin 159: None
        '''
        bin_num = 0
        for i in self._oahd:
            print 'bin ' + str(bin_num) + ': ' + str(i)
            bin_num = bin_num + 1


class BSTNode(object):
    def __init__(self, key=None, value=None):
        super(BSTNode, self).__init__()
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.parent = None


class BinarySearchTreeDict(object):

    def __init__(self):
        super(BinarySearchTreeDict, self).__init__()
        self.item_count = 0
        self.root = None

    def height(self):
        '''
        Returns keys in the tree in inorder one at a time
        >>> obj = generateBinarySearchTree()
        >>> obj.height()
        12
        '''
        if self.root is None:
            return 0
        elif self.root.right is None and self.root.left is None:
            return 1
        else:
            stack = []
            stack.append(self.root)
            tree_height = 0
            prev = None
            while len(stack) != 0:
                node = stack[-1]
                if prev is None or prev.left is node or prev.right is node:
                    if node.left is not None:
                        stack.append(node.left)
                    elif node.right is not None:
                        stack.append(node.right)
                elif node.left is prev:
                    if node.right is not None:
                        stack.append(node.right)
                else:
                    stack.pop()
                prev = node
                if len(stack) > tree_height:
                    tree_height = len(stack)
            return tree_height

    def inorder_keys(self):
        '''
        Returns keys in the tree in inorder one at a time
        >>> obj = generateBinarySearchTree()
        >>> str = (6, 28, 31, 282, 482, 533, 590, 619, 682, 846, 901,
        ...        1004, 1244, 1256, 1297, 1317, 1546, 1643, 1847, 2132,
        ...        2180, 2207, 2211, 2230, 2231, 2243, 2286, 2298, 2376,
        ...        2492, 2529, 2639, 2657, 2935, 2972, 3191, 3228, 3246,
        ...        3302, 3334, 3399, 3494, 3666, 3962, 3982, 4004, 4055,
        ...        4078, 4255, 4316, 4404, 4437, 4504, 4515, 4529, 4739,
        ...        5002, 5299, 5410, 5499, 5510, 5517, 5545, 5686, 5745,
        ...        5795, 5953, 5961, 5978, 6270, 6456, 6532, 6649, 6699,
        ...        6814, 7196, 7220, 7498, 7583, 7748, 7951, 8000, 8049,
        ...        8170, 8332, 8441, 8600, 8644, 8728, 8734, 8904, 8974,
        ...        8987, 8998, 9019, 9177, 9390, 9397, 9865, 9983)
        >>> tuple(obj.inorder_keys()) == str
        True
        '''
        if self.root is None:
            return
        else:
            stack = []
            node = self.root
            while len(stack) != 0 or node is not None:
                if node is not None:
                    stack.append(node)
                    node = node.left
                else:
                    node = stack.pop()
                    yield node.key
                    node = node.right

    def postorder_keys(self):
        '''
        Returns keys in the tree in postorder one at a time
        >>> obj = generateBinarySearchTree()
        >>> str = (28, 282, 31, 6, 533, 482, 682, 619, 901,
        ...        1244, 1004, 1297, 1256, 846, 2132, 1847,
        ...        1643, 2211, 2207, 2180, 1546, 2231, 2286,
        ...        2298, 2243, 2492, 2639, 2529, 2935, 3191,
        ...        2972, 2657, 2376, 2230, 1317, 3246, 3228, 590, 3494,
        ...        3399, 3982, 3962, 4055, 4004, 3666, 4255, 4078, 4437,
        ...        4404, 4504, 4529, 4515, 5299, 5002, 4739, 4316, 3334,
        ...        3302, 5499, 5517, 5686, 5545, 5510, 5961, 5953, 6270,
        ...        5978, 5795, 6532, 6699, 6649, 6456, 5745, 5410, 7196,
        ...        7498, 7748, 7583, 7951, 7220, 8049, 8170, 8000, 8332,
        ...        8644, 8600, 8734, 8987, 9019, 8998, 8974, 8904, 8728,
        ...        8441, 9865, 9983, 9397, 9390, 9177, 6814)
        >>> tuple(obj.postorder_keys()) == str
        True
        '''
        if self.root is None:
            return
        else:
            stack = []
            node = self.root
            prev = None
            while len(stack) != 0 or node is not None:
                if node is not None:
                    stack.append(node)
                    node = node.left
                else:
                    peek = stack[-1]
                    if peek.right is not None and peek.right is not prev:
                        node = peek.right
                    else:
                        yield stack.pop().key
                        prev = peek

    def preorder_keys(self):
        '''
        Returns keys in the tree in preorder one at a time
        >>> obj = generateBinarySearchTree()
        >>> str = (6814, 5410, 3302, 590, 482, 6, 31, 28, 282, 533, 3228, 1317,
        ...        846, 619, 682, 1256, 1004, 901, 1244, 1297, 2230, 1546,
        ...        2180, 1643, 1847, 2132, 2207, 2211, 2376, 2243, 2231, 2298,
        ...        2286, 2657, 2529, 2492, 2639, 2972, 2935, 3191, 3246, 3334,
        ...        4316, 4078, 3666, 3399, 3494, 4004, 3962, 3982, 4055, 4255,
        ...        4739, 4515, 4504, 4404, 4437, 4529, 5002, 5299, 5745, 5510,
        ...        5499, 5545, 5517, 5686, 6456, 5795, 5978, 5953, 5961, 6270,
        ...        6649, 6532, 6699, 9177, 8441, 8332, 8000, 7220, 7196, 7951,
        ...        7583, 7498, 7748, 8170, 8049, 8728, 8600, 8644, 8904, 8734,
        ...        8974, 8998, 8987, 9019, 9390, 9397, 9983, 9865)
        >>> tuple(obj.preorder_keys()) == str
        True
        '''
        if self.root is None:
            return
        else:
            stack = []
            stack.append(self.root)
            while len(stack) != 0:
                node = stack.pop()
                yield node.key
                if node.right is not None:
                    stack.append(node.right)
                if node.left is not None:
                    stack.append(node.left)

    def items(self):
        ''' Print items in order in key: value format
        >>> obj = generateBinarySearchTree()
        >>> str = ('6: 19', '28: 72', '31: 64', '282: 70', '482: 11',
        ...        '533: 38', '590: 5', '619: 43', '682: 65', '846: 20',
        ...        '901: 73', '1004: 68', '1244: 77', '1256: 61', '1297: 99',
        ...        '1317: 17', '1546: 41', '1643: 80', '1847: 89', '2132: 90',
        ...        '2180: 75', '2207: 96', '2211: 97', '2230: 18', '2231: 45',
        ...        '2243: 31', '2286: 46', '2298: 42', '2376: 27', '2492: 58',
        ...        '2529: 51', '2639: 86', '2657: 32', '2935: 84', '2972: 71',
        ...        '3191: 74', '3228: 10', '3246: 50', '3302: 4', '3334: 7',
        ...        '3399: 37', '3494: 91', '3666: 25', '3962: 49', '3982: 54',
        ...        '4004: 44', '4055: 69', '4078: 24', '4255: 82', '4316: 12',
        ...        '4404: 67', '4437: 78', '4504: 30', '4515: 29', '4529: 79',
        ...        '4739: 23', '5002: 57', '5299: 59', '5410: 2', '5499: 40',
        ...        '5510: 28', '5517: 83', '5545: 34', '5686: 60', '5745: 3',
        ...        '5795: 9', '5953: 48', '5961: 94', '5978: 35', '6270: 66',
        ...        '6456: 6', '6532: 56', '6649: 52', '6699: 81', '6814: 0',
        ...        '7196: 85', '7220: 22', '7498: 93', '7583: 88', '7748: 92',
        ...        '7951: 63', '8000: 16', '8049: 55', '8170: 26', '8332: 14',
        ...        '8441: 8', '8600: 36', '8644: 87', '8728: 13', '8734: 47',
        ...        '8904: 15', '8974: 21', '8987: 95', '8998: 39', '9019: 98',
        ...        '9177: 1', '9390: 33', '9397: 53', '9865: 76', '9983: 62')
        >>> tuple(obj.items()) == str
        True
        '''
        if self.root is None:
            return
        else:
            stack = []
            node = self.root
            while len(stack) != 0 or node is not None:
                if node is not None:
                    stack.append(node)
                    node = node.left
                else:
                    node = stack.pop()
                    to_str = str(node.key) + ': ' + str(node.value)
                    yield to_str
                    node = node.right

    def __getitem__(self, key):
        ''' get item from tree given the key
        use: node = tree[key]
        >>> obj = generateBinarySearchTree()
        >>> print(obj[5686].value)
        60
        '''
        root = self.root
        while 1:
            if root is None:
                return
            elif root.key == key:
                return root
            elif root.key > key:
                root = root.left
            else:
                root = root.right

    def __setitem__(self, key, value):
        ''' set the node in the tree given the key and value
        use: tree[key] = value
        >>> obj = generateBinarySearchTree()
        >>> obj[1292] = 1002
        >>> 1292 in obj
        True
        >>> print(obj[1292].value)
        1002
        '''
        if self.root is None:
            self.root = BSTNode(key, value)
            self.item_count = self.item_count + 1
        else:
            root = self.root
            while 1:
                if root.key == key:
                    root.key = key
                    root.value = value
                    return
                elif root.key > key:
                    if root.left is not None:
                        root = root.left
                    else:
                        root.left = BSTNode(key, value)
                        root.left.parent = root
                        self.item_count = self.item_count + 1
                        return
                else:
                    if root.right is not None:
                        root = root.right
                    else:
                        root.right = BSTNode(key, value)
                        root.right.parent = root
                        self.item_count = self.item_count + 1
                        return

    def __delitem__(self, key):
        ''' delete an item from the tree given the key
        use: del(tree[key])
        >>> obj = generateBinarySearchTree()
        >>> del(obj[5686])
        >>> 5686 in obj
        False
        >>> for i in test_keys:
        ...     i in obj
        ...
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        False
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        '''
        node = self[key]
        if node is None:
            return
        elif node.right is None and node.left is None:
            if node.parent.right is node:
                node.parent.right = None
            else:
                node.parent.left = None
        elif node.right is None and node.left is not None:
            if node.parent.right is node:
                node.parent.right = node.left
                node = None
            else:
                node.parent.left = node.left
                node = None
        elif node.right is not None:
            temp = node.right
            while temp.left is not None:
                temp = temp.left
            node.key = temp.key
            node.value = temp.value
            temp.parent.left = None
            temp = None
        if self.item_count > 0:
            self.item_count = self.item_count - 1

    def __contains__(self, key):
        ''' check if the node is in the collection given the key
        use: key in tree
        >>> obj = generateBinarySearchTree()
        >>> 2935 in obj
        True
        >>> 9920 in obj
        False
        '''
        root = self.root
        while 1:
            if root is None:
                return False
            elif root.key == key:
                return True
            elif root.key > key:
                root = root.left
            else:
                root = root.right

    def __len__(self):
        ''' return the number of items in the tree
        >>> obj = generateBinarySearchTree()
        >>> len(obj)
        100
        '''
        return self.item_count

    def display(self):
        '''
        >>> test = BinarySearchTreeDict()
        >>> test[5] = 'test value'
        >>> test[2] = 'stuff'
        >>> test[7] = 'more'
        >>> test[4] = 'unimportant'
        >>> test[6] = 'blah'
        >>> test[8] = 'boring'
        >>> test.display()
        (2, 4, 5, 6, 7, 8)
        (5, 2, 4, 7, 6, 8)
        '''
        print tuple(self.inorder_keys())
        print tuple(self.preorder_keys())


def terrible_hash(bin):
    """A terrible hash function that can be used for testing.

    A hash function should produce unpredictable results,
    but it is useful to see what happens to a hash table when
    you use the worst-possible hash function.  The function
    returned from this factory function will always return
    the same number, regardless of the key.

    :param bin:
        The result of the hash function, regardless of which
        item is used.

    :return:
        A python function that can be passes into the constructor
        of a hash table to use for hashing objects.
    """
    def hashfunc(item):
        return bin
    return hashfunc


''' global test objects and functions
    maybe we could just use unittest and mock instead of these
    ugly doctests
'''
test_keys = [6814, 9177, 5410, 5745, 3302, 590, 6456, 3334,
             8441, 5795, 3228, 482, 4316, 8728, 8332, 8904,
             8000, 1317, 2230, 6, 846, 8974, 7220, 4739,
             4078, 3666, 8170, 2376, 5510, 4515, 4504, 2243,
             2657, 9390, 5545, 5978, 8600, 3399, 533, 8998,
             5499, 1546, 2298, 619, 4004, 2231, 2286, 8734,
             5953, 3962, 3246, 2529, 6649, 9397, 3982, 8049,
             6532, 5002, 2492, 5299, 5686, 1256, 9983, 7951,
             31, 682, 6270, 4404, 1004, 4055, 282, 2972, 28,
             901, 3191, 2180, 9865, 1244, 4437, 4529, 1643,
             6699, 4255, 5517, 2935, 7196, 2639, 8644, 7583,
             1847, 2132, 3494, 7748, 7498, 5961, 8987, 2207,
             2211, 9019, 1297]


def generateLinkedList():
    linkedListTest = SinglyLinkedList()
    for i in range(0, 100):
        item = (test_keys[i], i)
        linkedListTest.prepend(item)
    return linkedListTest


def generateChainHashTest():
    chainHashTest = ChainedHashDict(10, 0.8)
    for i in range(0, 100):
        chainHashTest[test_keys[i]] = i
    return chainHashTest


def generateOpenHash():
    openHashTest = OpenAddressHashDict()
    for i in range(0, 100):
        openHashTest[test_keys[i]] = i
    return openHashTest


def generateBinarySearchTree():
    bst = BinarySearchTreeDict()
    for i in range(0, 100):
        bst[test_keys[i]] = i
    return bst


def main():
    # all functionality ran through tests (doctest.testmod())
    pass


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    main()
