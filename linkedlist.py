import string

class Node:
    def __init__(self,data):
        self.data=data
        self.next=None

class LinkedList:
    def __init__(self):
        self.head=None
        self.size=0
    
    def append(self,data):
        if self.head is None:
            self.head=Node(data)
            self.size+=1
        else:
            current=self.head
            while current.next is not None:
                current=current.next
            current.next=Node(data)
            self.size+=1
    
    def prepend(self,data):
        if self.head is None:
            self.head=Node(data)
            self.size+=1
        else:
            new_node=Node(data)
            new_node.next=self.head
            self.head=new_node
            self.size+=1

    def printData(self):
        current=self.head
        if self.head is None:
            print("The list is empty")
        else:
            while current.next is not None:
                print(current.data)
                current=current.next
            print(current.data)
    def getAt(self,index):
        current_index=0
        current=self.head

        if index < self.size:
            if index==0:
                print(self.head.data)
            else:
                while current.next is not None:
                    current=current.next
                    current_index+=1
                    if current_index==index:
                        break
                print(current.data)
        else:
            print("List out of range")
    
    def insertAt(self,index,data):
        if index <= self.size:
            if index==0:
                self.prepend(data)
            elif index==1:
                new_node=Node(data)
                new_node.next=self.head.next
                self.head.next=new_node
            else:
                current=self.head
                current_index=0
                while current.next is not None:
                    current=current.next
                    current_index+=1
                    if (index-current_index)==1:
                        break
                new_node=Node(data)
                new_node.next=current.next.next
                current.next=new_node
        else:
            print("List out of range")


            
    
    def reverse(self):
        if self.head is None:
            print("List is empty")
        else:
            current=self.head
            while current.next is not None:
                current=current.next
            
    

ll=LinkedList()

ll.append(100)
ll.append(200)
ll.append(300)
ll.append(400)
ll.insertAt(4,250)
ll.append(500)

ll.printData()

print("*****************")

ll.getAt(4)