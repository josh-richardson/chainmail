import hashlib
import json


class MerkleTree:

    def __init__(self):
        self.queue = []
        self.levels = None
        self.isReady = False
        self.stale = False

    def add(self, item):
        self.queue.append(item)

    def process(self):
        self.stale = True

        base_len = len(self.queue)
        desired_len = self.nearest_sq2(base_len)
        for i in range(0, desired_len - base_len):
            self.queue.append(self.hash_item("pad"))
        levels = []
        current_level = list(map(lambda x: Node(x, False), self.queue))
        while len(current_level) != 1:

            current_len = len(current_level)
            parings = zip(current_level[:current_len // 2], current_level[current_len // 2:])
            new_current = []
            next_level = []

            for fst, snd in parings:
                parent_node = Node(hashlib.sha256(fst.sha_hash + snd.sha_hash).digest(), False)
                fst.parent = parent_node
                snd.parent = parent_node
                parent_node.left = fst
                parent_node.right = snd
                new_current.append(fst)
                new_current.append(snd)
                next_level.append(parent_node)

            levels.append(new_current)
            current_level = next_level
        levels.append(current_level)
        self.levels = levels
        self.isReady = True

    @staticmethod
    def nearest_sq2(number):
        nsq = 1
        while (2 ** nsq) < number:
            nsq += 1
        return 2 ** nsq

    @staticmethod
    def hash_item(data):
        return hashlib.sha256(data.encode("utf-8")).digest()

    def get_proof(self, data, get_json):

        relevant_item = next(filter(lambda x: x.sha_hash == data, self.levels[0]))
        proof = [str(relevant_item)]
        while relevant_item.parent is not None:
            parent = relevant_item.parent
            if parent.left == relevant_item:
                proof.append({'right': str(parent.right)})
            else:
                proof.append({'left': str(parent.left)})
            relevant_item = parent
        proof.append(str(relevant_item))
        if get_json:
            return json.dumps(proof)
        else:
            return proof

    @staticmethod
    def verify_proof(proof):

        target = proof[0]
        merkle_root = proof[-1]

        current = bytes.fromhex(target)
        for item in proof[1:-1]:
            if 'left' in item:
                current = hashlib.sha256(bytes.fromhex(item['left']) + current).digest()
            else:
                current = hashlib.sha256(current + bytes.fromhex(item['right'])).digest()

        return current.hex() == merkle_root


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
