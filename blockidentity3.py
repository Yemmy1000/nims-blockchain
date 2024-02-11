import hashlib as hasher
import datetime as date
import os
import uuid


# Define what a Snakecoin block is
class Block:
  def __init__(self, index, timestamp, data, previous_hash, eth_addr, user_id):
    self.index = index
    self.timestamp = timestamp
    self.data = data
    self.previous_hash = previous_hash
    self.hash = self.hash_block()
    self.eth_addr = eth_addr
    self.user_id = user_id

  
  def hash_block(self):
    sha = hasher.sha256()
    sha.update(str(self.index).encode() + str(self.timestamp).encode() + str(self.data).encode() + str(self.previous_hash).encode())
    return sha.hexdigest()

  def __str__(self):
    return (str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash)+ str(self.eth_addr)+ str(self.hash_data))

# Generate genesis block
def create_genesis_block():
  # Manually construct a block with
  # index zero and arbitrary previous hash
  return Block(0, date.datetime.now(), "Genesis Block", "0", "000000", "0000:0000")

# Generate all later blocks in the blockchain
def next_block(last_block):
  this_index = last_block.index + 1
  this_timestamp = date.datetime.now()
  this_data = user_data()
  this_hash = last_block.hash
  file_name = "addr_"+str(this_index)
  this_eth_addr = eth_addr(file_name)
  this_user_id = user_id(this_data, this_eth_addr)
  return Block(this_index, this_timestamp, this_data, this_hash, this_eth_addr, this_user_id)


def user_data():
  name =  input("Enter your data: ")
  return name 

def priv_key():
  name =  input("Enter your data: ")
  return name


def pub_key():
  name =  input("Enter your data: ")
  return name

def eth_addr(blk_file):
  file_obj = open(blk_file, 'r')
  sys_addr = file_obj.readline() 
  return sys_addr

def user_id(data, eth_addr):
  salt = uuid.uuid4().hex
  return hasher.sha256(salt.encode() + data.encode()).hexdigest() + ':' + salt

def store_user_id_in_file(index, b_hash, previous_hash, data, timestamp, eth_addr, user_id ):
  file_name = "user_"+str(index)
  file_obj = open(file_name, 'w')
  file_obj.write(str(index) + "\n"+ b_hash+ "\n"+previous_hash+ "\n"+data+ "\n"+str(timestamp)+ "\n"+eth_addr+ "\n"+user_id)
  file_obj.close()

def check_data(hashed_id, new_data):
    data, salt = hashed_id.split(':')
    return data == hasher.sha256(salt.encode() + new_data.encode()).hexdigest()

  
def main():
  # Create the blockchain and add the genesis block
  blockchain = [create_genesis_block()]
  previous_block = blockchain[0]

  # How many blocks should we add to the chain


  # after the genesis block
  num_of_blocks_to_add = 4

  # Add blocks to the chain
  for i in range(0, num_of_blocks_to_add):
    block_to_add = next_block(previous_block)
    new_data = block_to_add.data
    hashed_id = previous_block.user_id

    if check_data(hashed_id, new_data):
      print('Identity exist, No duplicate identity is allowed!!!')
    else:
      print('Identity is authentic!!!')
      blockchain.append(block_to_add)
      previous_block = block_to_add
      store_user_id_in_file(block_to_add.index, block_to_add.hash, block_to_add.previous_hash, block_to_add.data, block_to_add.timestamp, block_to_add.eth_addr, block_to_add.user_id )

  
      # Tell everyone about it!
      print("Block #{} has been added to the blockchain!".format(block_to_add.index))
      print("Hash: {}".format(block_to_add.hash))
      print("Previous Hash: {}".format(block_to_add.previous_hash))
      print("Data: {}".format(block_to_add.data))
      print("TimeStamp: {}".format(block_to_add.timestamp))
      print("System Address: {}".format(block_to_add.eth_addr))
      print("User Output ID: {}\n".format(block_to_add.user_id))
  
  


main()
