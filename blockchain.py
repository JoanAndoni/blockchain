# Module 1 - Create a Blockchain

# To be installed:
# Flask==0.12.2 with: pip install Flask==0.12.2

# Importing libraries
import datetime
import hashlib
import json
from flask import Flask, jsonify

# Part 1 - Building a Blockchain

# Define the class of the blockchain
class Blockchain:

    # Initial class that will define the chain(array of the blocks), then
    # the second step is to create the first block which will be the fisrt block
    # with the function defined in the same class
    def __init__(self):
        self.chain = []  # Define the chain empty
        self.create_block(proof=1, previous_hash="0")  # Create the first block

    # Function to create block in our chain which are going to take the proof and
    # the previous_hash as arguments to create the object to add it in our chain
    def create_block(self, proof, previous_hash):
        # Define the structure of our block
        block = {
            "index": len(self.chain) + 1,
            "timestamp": str(datetime.datetime.now()),
            "proof": proof,
            "previous_hash": previous_hash,
        }
        self.chain.append(block)  # Add the new block to our chain
        return block

    # Function that will retrn the last block of the chain ans that will allow
    # us to get the last block of the chain
    def get_previous_block(self):
        return self.chain[-1]  # Just return the last value of the chain

    # Function that will make the puzzle for the miners to make the new encription
    # for the new block
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        # Loop that will end util we check the validation of the encription
        while check_proof is False:
            # Operation that the miners will have to do, encripted with
            # SHA256 which are 64 characters // Solve new_proof**2 - previous_proof**2 //
            hash_operation = hashlib.sha256(
                str(new_proof ** 2 - previous_proof ** 2).encode()
            ).hexdigest()
            # Check if the encoded puzzle have 4 leading '0'
            if hash_operation[:4] == "0000":
                # If it's true then change the variable to true
                check_proof = True
            else:
                # Else you increment by one the new proof until you get the encode
                new_proof += 1
        # When you get out from the loop return the new_proof value
        return new_proof

    # Check our blockchain is right by checking two things:
    #   1. Check if each block has the correct proof of work: Hash with four leading 0
    #   2. Check that the previous hash of each block is equal
    # thats how you get a valid blockchain

    # Function that will encode a block
    def hash(self, block):
        # Make the block a string with the library json plus the procedure to encode the string for
        # the hashlib 256
        encoded_block = json.dumps(block, sort_keys=True).encode()
        # Make the hash
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):
        # Get the first block of our chain
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            # The block will be the first block in our chain
            block = chain[block_index]
            # Check if the previous hash of the hash is the same as our first block
            if block["previous_hash"] != self.hash(previous_block):
                return False
            # Check that the proof of our blockchain have four leading 0
            previous_proof = previous_block["proof"]
            proof = block["proof"]
            hash_operation = hashlib.sha256(
                str(proof ** 2 - previous_proof ** 2).encode()
            ).hexdigest()
            if hash_operation[:4] != "0000":
                return False
            previous_block = block
            block_index += 1
        # If there's nothing wrong then return true
        return True


# Part 2 - Mining our Blockchain

# Creating a Web App

# RUN THE CODE WITH THIS STEPS in the terminal
# $ export FLASK_APP=hello.py
# $ flask run
#  * Running on http://127.0.0.1:5000/{route you implement}
app = Flask(__name__)

# Creating a blockchain
blockchain = Blockchain()


@app.route("/mine_block", methods=["GET"])
# Mine a block
def mine_block():
    # You have to get first the last block of the chain
    previous_block = blockchain.get_previous_block()
    # Then get the proof of that block
    previous_proof = previous_block["proof"]
    # Make the search for the new proof of the blockchain
    proof = blockchain.proof_of_work(previous_proof)
    # Get the previous hash by making it with the previous block
    previous_hash = blockchain.hash(previous_block)
    # Create the new block after we have the correct proof
    block = blockchain.create_block(proof, previous_hash)
    # Create the response that we are going to return
    response = {
        "message": "Congratulations, you just mined a block",
        "index": block["index"],
        "timestamp": block["timestamp"],
        "proof": block["proof"],
        "previous_hash": block["previous_hash"],
    }
    # Return the http status plus the response made as json with the library jsonify
    return jsonify(response), 200


# Get the full blockchain
@app.route("/get_chain", methods=["GET"])
def get_chain():
    response = {"chain": blockchain.chain, "length": len(blockchain.chain)}
    return jsonify(response), 200


# Get the response if the chain is valid
@app.route("/is_valid", methods=["GET"])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {"message": "The Blockchain is valid."}
    else:
        response = {"message": "We have a problem. The Blockchain is not valid."}
    return jsonify(response), 200


app.run(host="0.0.0.0", port=5000)

