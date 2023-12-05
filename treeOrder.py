from CircularQueue import CircularQueue

def preorder(n):
    if n != None:
        print(n.data,end=' ')
        preorder(n.left)
        preorder(n.right)
def inorder(n):
    if n != None:
        inorder(n.left)
        print(n.data,end=' ')
        inorder(n.right)
def postorder(n):
    if n != None:
        postorder(n.left)
        postorder(n.right)
        print(n.data,end=' ')

def levelorder(root):
    queue = CircularQueue()
    queue.enqueue(root)
    while len(queue) > 0:
        n = queue.dequeue()
        if n != None:
            print(n.data)
            queue.enqueue(n.left)
            queue.enqueue(n.right)