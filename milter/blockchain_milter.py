#!/usr/bin/env python
import re
from io import BytesIO

import Milter


class BlockchainMilter(Milter.Base):

    def __init__(self):
        self.id = Milter.uniqueID()
        self.rgx = re.compile('[^a-zA-Z]')
        self.relevant_headers = ["To", "From", "Subject"]

    def _new_message(self):
        self.headers = ""
        self.relevant_headers = ["To", "From", "Subject"]
        self.msg_body = BytesIO()

    @Milter.noreply
    def connect(self, hostname, family, hostaddr):
        self._new_message()

    @Milter.noreply
    def body(self, chunk):
        self.msg_body.write(chunk)

    def eom(self):
        self.msg_body.seek(0)
        msg = self.msg_body.read().decode("utf-8")
        total_string = self.rgx.sub("", "{}{}".format(msg, self.headers))
        print(f"Message to hash: {total_string}")
        return Milter.ACCEPT


if __name__ == "__main__":
    print("Running")

    socketname = "/var/spool/postfix/blockchain_milter/blockchain_milter"
    timeout = 20000
    Milter.factory = BlockchainMilter
    Milter.runmilter("BaseMilter", socketname, timeout)
