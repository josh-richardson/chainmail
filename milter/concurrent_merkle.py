import time

from merkle_tree import MerkleTree
from threading import Thread
from concurrent.futures import Future


def call_future(fn, future, args, kwargs):
    try:
        call_result = fn(*args, **kwargs)
        future.set_result(call_result)
    except Exception as ex:
        future.set_exception(ex)


def threaded(fn):
    def threaded_wrapper(*args, **kwargs):
        future = Future()
        Thread(target=call_future, args=(fn, future, args, kwargs)).start()
        return future

    return threaded_wrapper


class ConcurrentMerkle:

    def __init__(self, arweave_adder):
        self.merkle = MerkleTree()
        self.arweave_adder = arweave_adder
        self.current_tx = None

    @threaded
    def start_running(self):
        while True:
            time.sleep(5)
            self.merkle.process()
            root_hash = str(self.merkle.levels[-1][0])
            if root_hash != "5b34ffae04f55299b2d71f580b3bf392a4ef6ffd047de6bfc4c7d44d495a015f":
                self.current_tx = self.arweave_adder.add_blockchain(root_hash)
            self.merkle = MerkleTree()

    @threaded
    def get_tx(self):
        while self.current_tx is None:
            time.sleep(0.1)
        return self.current_tx

    @threaded
    def add(self, item, merkle):
        merkle.add(item)
        while not merkle.isReady:
            time.sleep(0.1)

        return merkle.get_proof(item, False)

    def verify(self, proof):
        return self.merkle.verify_proof(proof)
