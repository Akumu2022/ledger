import os
from abc import ABC, abstractmethod
from tronpy import Tron
from tronpy.keys import PrivateKey


class Signer(ABC):
    @abstractmethod
    async def sign_and_broadcast(self, tx_payload: dict) -> str:
        pass


class EnvSigner(Signer):
    def __init__(self):
        key = os.getenv("TRON_PRIVATE_KEY")
        if not key:
            raise Exception("TRON_PRIVATE_KEY not set")

        self.private_key = PrivateKey(bytes.fromhex(key))
        self.client = Tron()

    async def sign_and_broadcast(self, tx_payload: dict) -> str:
        txn = (
            self.client.trx.contract(tx_payload["contract"])
            .functions.transfer(
                tx_payload["to"],
                int(tx_payload["amount"])
            )
            .with_owner(self.private_key.public_key.to_base58check_address())
            .build()
            .sign(self.private_key)
        )

        result = txn.broadcast()
        return result["txid"]
