import hashlib
import json
import time
import tornado
from tornado import web
import datetime


class Block():
    def __init__(self, index, prev_hash, timestamp, data, hash):
        self.index = index
        self.prev_hash = prev_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash

    def get_json(self):
        return json.dumps(self.__dict__)

    def get_dict(self):
        return self.__dict__

def calculateHash(index, prev_hash, timestamp, data):
    m = hashlib.sha256()
    m.update(str(index) + prev_hash + str(timestamp) + data)
    return m.hexdigest()


def parse_from_json(jsoni):
    bb = json.loads(jsoni)
    bb = Block(bb['index'], bb['prev_hash'], bb['timestamp'], bb['data'], bb['hash'])
    return bb

def genesisBlock():
    """
    Returns next block
    now only returns genesis block
    :return:
    """
    return Block(0, "0", 1465154705, "my genesis block!!",
                 "816534932c2b7154836da6afc367695e6337db8a921823784c14378abed4f7d7");


def generataNextBlock(prev_block, data):
    next_index = int(prev_block.index) + 1
    next_timestamp = time.mktime(datetime.datetime.now().timetuple())
    next_hash = calculateHash(next_index, prev_block.hash, next_timestamp, data)
    return Block(next_index, prev_block.hash, next_timestamp, data, next_hash)


def isValidBlock(new_block, prev_block):
    valid_index = new_block.index == prev_block.index + 1
    valid_prev_hash = prev_block.hash == new_block.prev_hash
    valid_hash = calculateHash(new_block.index, prev_block.hash, new_block.timestamp, new_block.data) == new_block.hash
    return valid_index and valid_prev_hash and valid_hash


def isValidChain(chain):
    # if there is only genesis block or empty passes test
    if len(chain) < 2:
        return True
    else:
        return all(isValidBlock(block, prev_bloc) for prev_bloc, block in zip(chain, chain[1:]))


def choose_longest(chain, prev_chain):
    if (isValidChain(chain), len(chain) > len(prev_chain)):
        return chain
    else:
        return prev_chain
