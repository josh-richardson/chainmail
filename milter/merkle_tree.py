import hashlib
import json


class MerkleTree:

    def __init__(self):
        self.queue = []
        self.levels = None

    def add(self, item):
        pass

    def process(self):
        pass

    def get_proof(self, data, get_json=False):
        pass

    @staticmethod
    def verify_proof(proof):
        pass



class Node:
    def __init__(self, sha_hash, should_hash):
        self.parent = None
        self.left = None
        self.right = None
        if should_hash:
            self.sha_hash = hashlib.sha256(sha_hash.encode("utf-8")).digest()
        else:
            self.sha_hash = sha_hash

    def __str__(self):
        return self.sha_hash.hex()

    def __repr__(self):
        return self.sha_hash.hex()