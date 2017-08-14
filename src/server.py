from tornado import web
import json
import requests
from ayla import *

QUERY_LATEST = "Query Latest"

QUERY_ALL = "Query All"

RESPONSE_BLOCKCHAIN = "Response Blockcahing"

class InitMessageHandler():
    def __init__(self,message,address):

        message = json.loads(message)

        if message.type == QUERY_LATEST:
            response = json.dumps({
                'type': RESPONSE_BLOCKCHAIN,
                'data': json.dumps(blockchain[-1])
            })
            requests.post(address,response)

        elif message.type == QUERY_ALL:
            response = json.dumps({
                'type': RESPONSE_BLOCKCHAIN,
                'data': json.dumps(blockchain)
            })
            requests.post(address,response)

        elif message.type == RESPONSE_BLOCKCHAIN:
            #do something
            return

class BlocksHandler(web.RequestHandler):
    def get(self):
        self.write(json.dumps(blockchain))

class MineBlocks(web.RequestHandler):

    def post(self):
        block = parse_from_json(self.request.body)
        if block:
            new_block = generataNextBlock(block,"hello world");
        blockchain.append(new_block.get_dict())
        self.write(json.dumps(blockchain))
        print('block added: ' + json.dumps(new_block.get_dict()))

class AddPeer(web.RequestHandler):

    def post(self):

        peers = self.request.body

        for peer in peers:
            peers.append(peer)

        self.write("OK")

class Peers(web.RequestHandler):

    def get(self):
        self.write(json.dumps(peers))

def make_app():
    return web.Application([
        (r"/blocks", BlocksHandler),
        (r"/mine", MineBlocks),
        (r"/addPeer",AddPeer),
        (r"/peers",Peers)
    ])
1
def server():
    app = make_app()
    print("starts server")
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()


blockchain = []

peers = []

server()