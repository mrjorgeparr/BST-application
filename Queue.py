

"""Implementation of Queue for phase 2, based on a dlist"""

from dlist import DList
import random


class Queue(DList):

    def __init__(self):
        super(Queue, self).__init__()


    def put(self, el):
        self.addLast(el)

    def get(self):
        s = self._head.elem
        self.removeFirst()
        return s

    def empty(self):
        return len(self) == 0

    def __getitem__(self, index):
        return self.getAt(index)

    def print(self):
        print("\nPrinting all elements of the queue\n")
        for i in range(len(self)):
            print("Element number: ", i, ":\t", self[i])

    def top(self):
        return self._head.elem



def test():
    print("\n Tests for class 'Queue'")
    #create instance
    q = Queue()

    #testing method enqueue
    for i in range(10): q.put(i)

    #print all elements
    q.print()

    r = random.randint(0,len(q))

    #testing __getiitem__()
    print("Element ",r,":\t ", q[r])

    #testing __len__()
    print("Length of queue: ", len(q))

    #testing isEmpty()
    print("Empty status: ", q.empty())


    print("\nRemoving element from queue: ",q.get())
    print("\nRemoving element from queue: ", q.get())
    print("\nRemoving element from queue: ", q.get())

    q.print()


def test():
    print("\n Tests for class 'Queue2'")
    #create an instance
    q = Queue()

    #testing method enqueue
    for i in range(10): q.put(i)

    #testing method print
    q.print()


    #testing method dequeue
    print("\nRemoving top element...")
    q.get()
    print("\nRemoving top element...")
    q.get()

    print("\n")

    r = random.randint(0, len(q))

    # testing __getiitem__()
    print("Element ", r, ":\t ", q[r])


    #print all elements again
    q.print()

    print("\nLength of q: ", len(q))
    print("Empty status: ", q.empty())

if __name__ == '__main__':
    test()


