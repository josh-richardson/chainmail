#!/usr/bin/env python
import json
import re
from io import BytesIO

import Milter


class BlockchainMilter(Milter.Base):

    def __init__(self):
        self.id = Milter.uniqueID()
        self.rgx = re.compile('[^a-zA-Z]')
        self.relevant_headers = ["To", "From", "Subject"]

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
