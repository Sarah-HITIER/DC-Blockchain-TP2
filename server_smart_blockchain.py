## 1
import hashlib
import json
from time import time
from urllib.parse import urlparse

from flask import Flask, jsonify, request
from Smart_Blockchain import Smart_Blockchain 

# Instantiate the Node
app = Flask(__name__)

# Instantiate the Smart_Blockchain
blockchain = Smart_Blockchain()


## 2
@app.route('/mine', methods=['GET'])
def mine():
    """
    Cette méthode est associée à l'endpoint /mine et est appelée lorsqu'une requête GET est reçue à cet endpoint.
    En appelant cette méthode, un mineur (node) forge un nouveau bloc en l'ajoutant à la chaîne et retourne les détails de ce bloc.

    :return: Un objet JSON avec les détails du nouveau bloc et le statut HTTP 200 (OK).
    """
    # Récupération du dernier bloc dans la chaîne
    last_block = blockchain.last_block

    # Calcul du hash du dernier bloc
    previous_hash = blockchain.hash_block(last_block)

    # Création d'un nouveau bloc dans la blockchain
    block = blockchain.new_block(previous_hash)

    # Construction de la réponse JSON
    response = {
        'message': "New block forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'previous_hash': block['previous_hash'],
    }

    # Retour de la réponse JSON avec le statut HTTP 200 (OK)
    return jsonify(response), 200


## 3
@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    """
    Cette méthode est associée à l'endpoint /transactions/new et est appelée lorsqu'une requête POST est reçue à cet endpoint.
    L'utilisateur peut créer une nouvelle transaction en fournissant les détails nécessaires via une requête POST.

    :return: Un objet JSON avec un message indiquant que la transaction sera ajoutée à un bloc spécifique et le statut HTTP 201 (Created).
    """
    # Récupération des données POST
    values = request.get_json()

    # Vérification des champs requis
    required = ['sender', 'amount', 'recipient']
    if not all(k in values for k in required):
        return jsonify({'message': 'Missing values'}), 400

    # Création d'une nouvelle transaction
    index = blockchain.new_transaction(values['sender'], values['amount'], values['recipient'])

    # Construction de la réponse JSON
    response = {'message': f'Transaction will be added to Block {index}'}

    # Retour de la réponse JSON avec le statut HTTP 201 (Created)
    return jsonify(response), 201


## 4
@app.route('/chain', methods=['GET'])
def full_chain():
    """
    Cette méthode est associée à l'endpoint /chain et est appelée lorsqu'une requête GET est reçue à cet endpoint.
    Un utilisateur peut récupérer la liste complète des blocs de la chaîne et sa longueur.

    :return: Un objet JSON avec les détails de la chaîne de blocs et le statut HTTP 200 (OK).
    """
    # Construction de la réponse JSON
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }

    # Retour de la réponse JSON avec le statut HTTP 200 (OK)
    return jsonify(response), 200


## 5
if __name__ == '__main__':
    import sys
    app.run(host='0.0.0.0', port=sys.argv[1])



### Étape 4
## 2.
@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()
    nodes = values.get('nodes')
    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201


## 3.2
@app.route('/smart/chain', methods=['GET'])
def smart_chain():
    replaced = blockchain.smart_chain()
    if replaced:
        response = {
            'message': 'Smart chain update by bpsc',
            'smart chain': blockchain.chain,
            'length': len(blockchain.chain)
        }
    else:
        response = {
            'message': 'Unsuccessful: Please try again',
            'old chain': blockchain.chain,
            'length': len(blockchain.chain)
        }
    return jsonify(response), 200