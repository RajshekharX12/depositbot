class ReceiveUSDT:
    def get_wallet_address(self, user_wallets, user_id):
        """Returns the user's wallet address."""
        wallet = user_wallets.get(user_id)
        if wallet:
            return wallet["public_address"]
        return None
