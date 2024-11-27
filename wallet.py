from tronpy.keys import PrivateKey

class WalletManager:
    def __init__(self):
        self.user_wallets = {}  # In-memory store for user wallets

    def create_wallet(self, user_id):
        """Creates a wallet for a user if it doesn't already exist."""
        if user_id in self.user_wallets:
            return self.user_wallets[user_id]["public_address"]

        private_key = PrivateKey.random()
        public_address = private_key.address.base58
        self.user_wallets[user_id] = {
            "private_key": private_key.hex(),
            "public_address": public_address,
        }
        return public_address

    def get_wallet_address(self, user_id):
        """Returns the wallet address of the user."""
        return self.user_wallets.get(user_id, {}).get("public_address")

    def get_wallet_private_key(self, user_id):
        """Returns the private key of the user."""
        return self.user_wallets.get(user_id, {}).get("private_key")
