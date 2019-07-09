import os
import tempfile
import subprocess

arweave_keyfile = os.environ.get('ARWEAVE_KEYFILE')


class ArweaveAdder():

    # If I had time I'd write a proper python library seeing as there doesn't seem to be one, but I started this
    # hackathon with 48 hours left so subprocess wrapper will have to do

    def add_blockchain(self, hash):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as fp:
            fp.write(hash.encode("utf-8"))
            fp.close()
        result = str(subprocess.run(
            ["arweave", "deploy", fp.name, "--key-file", arweave_keyfile, "--force-skip-confirmation"],
            capture_output=True).stdout.decode("utf-8"))
        tx_hash = result[result.index("ID:") + 4:result.index("Price:") - 1]
        print(f"Added to arweave blockchain: {tx_hash}")
        return tx_hash
