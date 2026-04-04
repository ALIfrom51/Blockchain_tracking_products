import hashlib   # Pour calculer les hash SHA-256
import json      # Pour convertir les données en texte
import os        # Pour créer les dossiers si besoin
from datetime import datetime # Pour enregistrer la date et l'heure de chaque bloc

DATA_FILE = "data/chain.json"

def hash_data(data):
    """Return a SHA-256 hash of the given data.

    The data is converted to a JSON string with sorted keys so that
    the hash is stable for the same content.
    """
    data_string = json.dumps(data, sort_keys=True).encode('utf-8')
    return hashlib.sha256(data_string).hexdigest()

def create_genesis_block():
    """Create the genesis block, which is the first block in the chain."""
    genesis_block = {
        "index": 0,
        "timestamp": datetime.utcnow().isoformat(),
        "data": "Genesis Block",
        "previous_hash": "0"
    }
    genesis_block["hash"] = hash_data(genesis_block)
    return genesis_block    

def load_chain():       
    """Load the blockchain from the JSON file, or create a new one if it doesn't exist."""
    if not os.path.exists(DATA_FILE):
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        chain = [create_genesis_block()]
        save_chain(chain)
    else:
        with open(DATA_FILE, 'r') as f:
            chain = json.load(f)
    return chain

def save_chain(chain):
    """Save the blockchain to the JSON file."""
    with open(DATA_FILE, 'w') as f:
        json.dump(chain, f, indent=4)

def add_block(data):
    """Add a new product with the given data to the blockchain."""
    chain = load_chain()
    last_block = chain[-1]
    new_block = {
        "index": last_block["index"] + 1,
        "timestamp": datetime.utcnow().isoformat(),
        "data": data,
        "previous_hash": last_block["hash"]
    }
    new_block["hash"] = hash_data(new_block)
    chain.append(new_block)
    save_chain(chain)
    return new_block


def track_product(product_id, name, quantity, location, recipient_location):
    """Track a new product and save the initial delivery record in the blockchain."""
    product_data = {
        "type": "package",
        "product_id": product_id,
        "name": name,
        "quantity": quantity,
        "location": location,
        "recipient_location": recipient_location,
        "status": "Enregistré",
        "tracked_at": datetime.utcnow().isoformat()
    }
    return add_block(product_data)


def update_package_status(product_id, status, location, note=None):
    """Add a delivery update for a package during its transport."""
    event_data = {
        "type": "delivery_event",
        "product_id": product_id,
        "status": status,
        "location": location,
        "note": note or "",
        "event_at": datetime.utcnow().isoformat()
    }
    return add_block(event_data)


def delete_product(product_id, reason):
    """Mark a product as deleted in the blockchain (immutable deletion event)."""
    deletion_data = {
        "type": "deletion",
        "product_id": product_id,
        "reason": reason,
        "deleted_at": datetime.utcnow().isoformat()
    }
    return add_block(deletion_data)


def get_product_by_hash(hash_code):
    """Return the block that contains the given hash code."""
    for block in load_chain():
        if block.get("hash") == hash_code:
            return block
    return None


def get_product_history(product_id):
    """Return all blockchain blocks for the specified product ID."""
    return [
        block for block in load_chain()
        if isinstance(block.get("data"), dict) and block["data"].get("product_id") == product_id
    ]


def trace_product(product_id):
    """Alias for get_product_history to trace a product by its ID."""
    return get_product_history(product_id)


def verify_block(block):
    """Verify that the stored hash matches the recomputed hash for the block."""
    block_copy = {key: value for key, value in block.items() if key != "hash"}
    return hash_data(block_copy) == block.get("hash")


def verify_hash(hash_code):
    """Find a block by hash and verify its integrity."""
    block = get_product_by_hash(hash_code)
    if block is None:
        return None
    return verify_block(block)


def reset_chain():
    """Reset the blockchain to its initial state with only the genesis block."""
    chain = [create_genesis_block()]
    save_chain(chain)
    return chain


def get_chain():
    """Return the current blockchain."""
    return load_chain()     

