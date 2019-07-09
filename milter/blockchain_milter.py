#!/usr/bin/env python
import hashlib
import json
import re
from io import BytesIO

import Milter

from arweave_adder import ArweaveAdder
from concurrent_merkle import ConcurrentMerkle


class BlockchainMilter(Milter.Base):

    def __init__(self):
        self.id = Milter.uniqueID()
        self.relevant_headers = ["To", "From", "Subject"]
        self.blockchain_merkle = ConcurrentMerkle(ArweaveAdder())
        self.blockchain_merkle.start_running()

    def _new_message(self):
        self.headers = {}
        self.msg_body = BytesIO()

    @Milter.noreply
    def connect(self, hostname, family, hostaddr):
        self._new_message()
        return Milter.CONTINUE

    @Milter.noreply
    def body(self, chunk):
        self.msg_body.write(chunk)
        return Milter.CONTINUE

    def eom(self):
        self.msg_body.seek(0)
        msg = self.msg_body.read().decode("utf-8")
        total_string = json.dumps({"message": msg, "headers": self.headers})
        print(f"Message to hash: {total_string}")

        proof = self.blockchain_merkle.add(hashlib.sha256(total_string.encode("utf-8")).digest(),
                                           self.blockchain_merkle.merkle)
        proof_result = proof.result()

        tx = self.blockchain_merkle.get_tx()
        tx_result = tx.result()

        return_proof = json.dumps({"tx": tx_result, "proof": proof_result})
        print(return_proof)

        return Milter.ACCEPT

    @Milter.noreply
    def header(self, key, value):
        if key in self.relevant_headers:
            self.headers[key.lower()] = value.lower()
        return Milter.CONTINUE


if __name__ == "__main__":
    print("Running")

    socketname = "/var/spool/postfix/blockchain_milter/blockchain_milter"
    timeout = 20000
    Milter.factory = BlockchainMilter
    Milter.runmilter("BaseMilter", socketname, timeout)
