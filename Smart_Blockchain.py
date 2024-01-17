## 2.1
import hashlib
import json
from time import time

## 3
class Smart_Blockchain:

## 3.1
    def __init__(self):
        self.current_transactions = []
        self.chain = []
        self.new_block(1)
        self.nodes = set() # Étape 4 : 1.1

## 3.2 - 4
    def new_block(self, previous_hash):
        """
        Crée un nouveau bloc dans la Smart Blockchain.

        :param previous_hash: Le hash précédent dans la chaîne.
        :return: Le nouveau bloc créé.
        """
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'previous_hash': previous_hash,
        }
        # Réinitialisation de la liste des transactions en cours
        self.current_transactions = []
        # Ajout du bloc à la chaîne
        self.chain.append(block)
        return block

## 5
    def new_transaction(self, sender, amount, recipient):
        """
        Crée une nouvelle transaction pour le prochain bloc miné.

        :param sender: Adresse de l'expéditeur.
        :param amount: Montant envoyé par l'expéditeur.
        :param recipient: Adresse du destinataire.
        :return: L'index du bloc qui contiendra cette transaction.
        """
        fees = 0.00005  # Frais de transaction à 0.00005 pour prévenir le spam

        transaction = {
            'sender': sender,
            'amount_send': amount,
            'bpsc': 'bpsc_wallet_address',
            'amount_bpsc': amount * fees,
            'recipient': recipient,
            'amount_receive': amount * (1 - fees),
        }

        # Ajout de la transaction à la liste des transactions en cours
        self.current_transactions.append(transaction)

        # Retourne l'index du bloc qui contiendra cette transaction
        return self.last_block['index'] + 1

## 6
    @property
    def last_block(self):
        """
        Retourne le dernier bloc de la chaîne.

        :return: Le dernier bloc de la chaîne.
        """
        return self.chain[-1]


## 7
    def hash_block(self, block):
        """
        Retourne le hash du bloc.

        :param block: Le bloc pour lequel calculer le hash.
        :return: Le hash du bloc.
        """
        # Conversion du bloc en chaîne JSON triée
        block_string = json.dumps(block, sort_keys=True).encode()

        # Application de la fonction de hachage SHA-256 pour obtenir le hash
        return hashlib.sha256(block_string).hexdigest()



### Étape 4
## 1.2
    def register_node(self, address):
        """
        Add a new node to the list of nodes
        :param address: Address of node. Eg. 'http://192.168.0.5:5000'
        """
        parsed_url = urlparse(address)
        if parsed_url.netloc:
            self.nodes.add(parsed_url.netloc)
        elif parsed_url.path:
            # Accepts an URL without scheme like '192.168.0.5:5000'.
            self.nodes.add(parsed_url.path)
        else:
            raise ValueError('Invalid URL')


## 3.1
def smart_chain(self):
    """
    All nodes can receive the smart_chain
    """
    schain = None
    response = requests.get(f'http://127.0.0.1:5000/chain')
    if response.status_code == 200:
        schain = response.json().get('chain')

    if schain:
        self.chain = schain
        return True
    return False


## 3.2
