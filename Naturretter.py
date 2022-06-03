#!/usr/bin/env python
# coding: utf-8

# In[ ]:


mode = " "


# In[ ]:


# Start
import datetime as d # import the datetime library for our block timestamp and rename it as d for simplicity while typing 
import hashlib as h # import the library for hashing our block data and rename it as h for simplicity while typing 


class Block: # create a Block class
    def __init__(self, index, timestamp, role, company_name, product, quantity, expiry_date, prevhash): # declare an initial method that defines a block, a block contains the following information
        self.index = index 
        self.timestamp = timestamp
        self.role = role
        self.company_name = company_name
        self.product = product
        self.quantity = quantity
        self.expiry_date = expiry_date
        self.prevhash = prevhash
        self.hash = self.hashblock()

    def hashblock (self): # define a method for data encryption, this method will retain a hash of the block
        block_encryption=h.sha256() # We need a sha256 function to hash the content of the block, so let's declare it here
        data = (str(self.index)+str(self.timestamp)+str(self.role)+str(self.company_name)+str(self.product)+str(self.quantity)+str(self.expiry_date)+str(self.prevhash))
        block_encryption.update(data.encode('utf-8')) # to encrypt the data in the block, We need just to sum everything and apply the hash function on it
        return block_encryption.hexdigest() # let's return that hash result 
    
    @staticmethod # declaring a static method for the genesis block
    def genesisblock(): # delcare a function for generating the first block named genesis
        global mode
        company_name = input("Country of origin or Company name: \n")
        product = input("Product or Service name: \n")
        quantity = input("Quantity: \n")
        expiry_date = input("Expiry date of the batch of the product (yyyy-mm-dd): \n")
        return Block(0, d.datetime.now(), mode, company_name, product, quantity, expiry_date, " ") # return the genesis block
    
    @staticmethod # let's declare another static method to get the next block
    def newblock(lastblock): # get the next block, the block that comes after the previous block (prevblock+1)
        index = lastblock.index+1 # the id of this block will be equals to the previous block + 1, which is logic
        hashblock = lastblock.hash # the hash of this block
        global mode
        company_name = input("Country of origin or Company name: \n")
        product = input("Product or Service name: \n")
        quantity = input("Quantity: \n")
        expiry_date = input("Expiry date of the batch of the product (yyyy-mm-dd): \n")
        return Block(index, d.datetime.now(), mode, company_name, product, quantity, expiry_date, hashblock) # return the entire block


# In[ ]:


def welcome():
    return print("Welcome to Naturretter\nWhere we aim to reduce food waste and provide quality assurance of your food\nBy tracking the food supply chain")


# In[ ]:


def getMode():
    return input("\nPlease enter user mode: \n[Upstream Producer, Manufacture or Shipping Company, Retailers, Customer]\nOr enter [query-all] to check all registered products: ")


# In[ ]:


import pickle
def store():
    global blockchain
    # open a pickle file
    filename = 'chains.pk'
    with open(filename, 'ab') as fi:
        # dump your data into the file
        pickle.dump(blockchain, fi)
    return


# In[ ]:


def read(hashInput):
    f = open("chains.pk", 'rb')
    while True:
        try:
            Object = pickle.load(f)
            for i in range(0, len(Object)):
                if hashInput == Object[i].hash:
                    return Object
        except EOFError:
            print("\nThe product information you entered is not clear or the source of the product is unknown!")
            print("Please confirm that the entered hash code is correct, otherwise please pay attention to the quality of the product!\n")
            break
    f.close()
    return productQuery()


# In[ ]:


def update(hashInput):
    checkBit = 0 #False
    f = open("chains.pk", 'rb+')
    chainList = []
    while True:
        try:
            Object = pickle.load(f)
            for i in range(0, len(Object)):
                if hashInput == Object[i].hash:
                    checkBit = 1
                    prevblock = Object[len(Object) - 1]
                    addblock = Block.newblock(prevblock)
                    Object.append(addblock)
                    print("\nHash of the block: {}\n".format(Object[len(Object) - 1].hash))
            chainList.append(Object)
        except EOFError:
            break
    if checkBit == 0:
        print("\nThe product information you entered is not clear or the source of the product is unknown!")
        print("Please confirm that the entered hash code is correct!\n")
        return createBlock()
    f.seek(0)
    f.truncate()
    
    for i in range(len(chainList)):
        pickle.dump(chainList[i], f)
    
    f.close()


# In[ ]:


def createGenesisBlock():
    global blockchain
    blockchain = [Block.genesisblock()]
    print("\nHash of the block: {}\n".format(blockchain[len(blockchain) - 1].hash))
    store()
    return blockchain

def createBlock():
    hashInput = input("Please type in hash code of the product\nOr enter [Home] to navigate to Home page: ")
    if hashInput == "Home":
        return switch()
    update(hashInput)
    #prevblock = blockchain[len(blockchain) - 1]
    #addblock = Block.newblock(prevblock)
    #blockchain.append(addblock)
    return 

def choose_operation():
    if(int(input("Select operations code, 1 for uploading data and 2 for product query: ")) == 1):
        return createBlock()
    else:
        return leftoverQuery()

def productQuery():
    hashInput = input("Please type in hash code of the product\nOr enter [Home] to navigate to Home page: ")
    if hashInput == "Home":
        return switch()
    blockchain = read(hashInput)
    for i in range (0, len(blockchain)):
        print("\nBlock ID #{} ".format(blockchain[i].index))
        print("Timestamp: {}".format(blockchain[i].timestamp))
        print("User mode: {}".format(blockchain[i].role))
        print("Country of Origin or Company Name: {}".format(blockchain[i].company_name))
        print("Product: {}".format(blockchain[i].product))
        print("Quantity: {}".format(blockchain[i].quantity))
        print("Expiry Date: {}".format(blockchain[i].expiry_date))
        print("Hash of the block: {}".format(blockchain[i].hash))
        print("Previous Block Hash: {}".format(blockchain[i].prevhash))
        print("--------------------------------------------------------\n")
    return

def default():
    print("\nSorry, please enter as a valid user mode!")
    return switch()


# In[ ]:


def leftoverQuery():
    hashInput = input("Please type in hash code of the product\nOr enter [Home] to navigate to Home page: ")
    if hashInput == "Home":
        return switch()
    blockchain = read(hashInput)
    product = blockchain[len(blockchain) - 1].product
    leftovers = []
    f = open("chains.pk", 'rb')
    while True:
        try:
            Object = pickle.load(f)
            if product == Object[len(Object) - 1].product:
                if Object[len(Object) - 1].role == "retailers":
                    leftovers.append(Object[len(Object) - 1])
        except EOFError:
            break
    f.close()
    for i in range(0, len(leftovers)):
        print("\nBlock ID #{} ".format(leftovers[i].index))
        print("Timestamp: {}".format(leftovers[i].timestamp))
        print("User mode: {}".format(leftovers[i].role))
        print("Country of Origin or Company Name: {}".format(leftovers[i].company_name))
        print("Product: {}".format(leftovers[i].product))
        print("Quantity: {}".format(leftovers[i].quantity))
        print("Expiry Date: {}".format(leftovers[i].expiry_date))
        print("Hash of the block: {}".format(leftovers[i].hash))
        print("Previous Block Hash: {}".format(leftovers[i].prevhash))
        print("--------------------------------------------------------\n")
    return


# In[ ]:


def listAll():
    f = open("chains.pk", 'rb+')
    while True:
        try:
            Object = pickle.load(f)
            for i in range (0, len(Object)):
                print("\nBlock ID #{} ".format(Object[i].index))
                print("Timestamp: {}".format(Object[i].timestamp))
                print("User mode: {}".format(Object[i].role))
                print("Country of Origin or Company Name: {}".format(Object[i].company_name))
                print("Product: {}".format(Object[i].product))
                print("Quantity: {}".format(Object[i].quantity))
                print("Expiry Date: {}".format(Object[i].expiry_date))
                print("Hash of the block: {}".format(Object[i].hash))
                print("Previous Block Hash: {}".format(Object[i].prevhash))
                print("--------------------------------------------------------\n")
        except EOFError:
            #print("Done")
            break
    f.close()


# In[ ]:


usrMode = {
    "upstream producer": createGenesisBlock,
    "manufacture or shipping company": createBlock,
    "retailers": choose_operation,
    "customer": productQuery,
    "query-all": listAll
}

def switch():
    global mode
    mode = getMode().lower()
    return usrMode.get(mode, default)()


# In[ ]:


welcome()


# In[ ]:


while True:
    switch()

