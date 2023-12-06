class BSTNode:
  def __init__(self,key,value):
    self.key = key
    self.value = value
    self.left = None
    self.right = None

def calc_height(n):
  if n == None:
    return 0
  hLeft = calc_height(n.left)
  hRight = calc_height(n.right)
  if hLeft > hRight:
    return hLeft + 1
  else:
    return hRight + 1
  
def calc_height_diff(n):
  if n ==None:
    return 0
  return calc_height(n.letf) - calc_height(n.right)

def rotateLL(A):
  B = A.left
  A.left = B.right
  B.right = A
  return B

def rotateRR(A):
  B = A.right
  A.right = B.left
  B.left = A
  return B

def rotateRL(A):
  B = A.right
  A.right = rotateLL(B)
  return rotateRR(A)

def rotataLR(A):
  B = A.left
  A.left = rotateRR(B)
  return rotateLL(A)

def insert(root,node):
  if root == None:
    return node
  if root.key == node.key:
    return root
  
  if node.key < root.key:
    root.left = insert(root.left,node)
  else:
    root.right = insert(root.right,node)

  bf = calc_height_diff(root)

  if bf > 1:
    if node.key < root.left.key:
      return rotateLL(root)
    else:
      return rotataLR(root)
  elif bf < -1:
    if node.key < root.right.key:
      return rotateRL(root)
    else:
      return rotateRR(root)
  return root