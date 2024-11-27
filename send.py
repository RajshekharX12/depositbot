from tronpy import Tron
from tronpy.keys import PrivateKey
from dotenv import load_dotenv
import os
import time

load_dotenv()
TRANSACTION_FEE = float(os.getenv("TRANSACTION_FEE", 0.5))
EARNING_FEE = float(os.getenv("EARNING_FEE", 0.5))
TOTAL_FEE = TRANSACTION_FEE + EARNING_FEE
USDT_CONTRACT_ADDRESS = os.getenv("USDT_CONTRACT_ADDRESS")

class SendUSDT:
    def __init__(self):
        self.client = Tron()

    def send_funds(self, sender_private_key, sender_address, recipient_address, amount):
        """Sends USDT to the recipient with error handling and retries."""
        amount_to_send = amount - TOTAL_FEE
        if amount_to_send <= 0:
            return "❌ Amount is too small to cover the fees! Please increase the amount."

        private_key = PrivateKey(bytes.fromhex(sender_private_key))
        usdt_contract = self.client.get_contract(USDT_CONTRACT_ADDRESS)

        attempts = 0
        max_retries = 3

        while attempts < max_retries:
            try:
                txn = (
                    usdt_contract.functions.transfer(recipient_address, int(amount_to_send * 1e6))
                    .with_owner(sender_address)
                    .fee_limit(100_000_000)
                    .build()
                    .sign(private_key)
                )
                txn_hash = txn.broadcast().wait()
                return f"✅ Transaction successful! 🎉\n\n💰 Amount Sent: {amount_to_send} USDT\n🔗 Transaction Hash: `{txn_hash}`"
            except Exception as e:
                attempts += 1
                time.sleep(2)
                if attempts >= max_retries:
                    return f"❌ Transaction failed after multiple attempts.\nError: {str(e)}"
