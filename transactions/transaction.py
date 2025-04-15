import dataclasses

@dataclasses.dataclass
class Transaction:
    id: str
    sender_id: int
    sender_name : str
    amount: int
    timestamp: int
    ip: str
    receiver_id: int
    receiver_name: str


