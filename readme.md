## Chainmail - Verifiable Email

### Overview:

Chainmail uses the Arweave blockchain in order to prove the content of emails passing through a mail server, and to provide a proof of the rough time at which this occurred. It's split into two parts: 

- A milter application which runs on a centralised web server, receives emails, and generates proofs. Once an email is received, relevant fields on the email are hashed, and a proof is generated. This proof is then sent to the sender and receiver(s) of the message so that they can verify it
- A single-page web app hosted on the Arweave blockchain which end users can use to verify the generated proofs.

### Can I demo this myself?

Yes! Send an email to a friend and cc `admin@chainmail.pw`. You and the friend should receive an additional email within a few minutes which contains a proof, and a link to verify that proof. Copy the proof to your clipboard, and open the link. Then paste the proof into the textbox, and click verify. If the proof is valid and has been mined (this may take up to 10 minutes!!), the application should show you a success screen with details and more information. 

### Decentralization:

The verifier web application is deployed on the Arweave blockchain, and proofs are also stored on the Arweave blockchain. However, proofs are generated from emails which are received using a centralised mail server. I'm not aware of any easy fix for this problem, whilst still retaining interoperability with email.

### Scalability:

As the Arweave blockchain has a block time of ~10 minutes, and a limited number of transactions per block are possible, a scaling solution is necessary so as to prevent congestion due to large numbers of emails being processed by Chainmail. For this reason, an internal Merkle tree structure is used. The Merkle tree allows for an arbitrary number of emails to be processed by the mail server, and for the root hash to be added to the Arweave blockchain. This solves the scalability issue, but means that email proofs must contain the necessary email hash, Merkle root, and all the necessary hashes to get from the leaf to the root (log(n)).

### Issues:

The greatest issue that I see is that the email which is actually received by the user is not necessarily the one that is verified - as the proof comes directly from the mail server, which you can't necessarily trust. For this reason, users must be vigilant, attempt to audit the code used by the verifier application, and ensure that the email body and headers verified are the same as the ones that they received.

This issue could be addressed by writing browser extensions or mail client extensions which automatically perform the verification process based on the hash of the received email itself, rather than a copy contained in the proof. Such a solution should be implemented, but I haven't had time.

### Future work & Comments:

Might productize this and add support for multiple backends. 

Separately, I noticed that a lot of deployed Arweave apps use arweave.net to initialise the Arweave JS API. I've avoided this as it would seem to break the decentralized aspect of the app.

### Libraries used:

The milter application uses pymilter (https://github.com/sdgathman/pymilter) and sendgrid (https://github.com/sendgrid/sendgrid-python)

The frontend uses jQuery (https://jquery.com/), Materliaze (https://materializecss.com/), and sha256.js (https://github.com/emn178/js-sha256)

### Video demo:

Coming soon :)