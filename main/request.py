from dataclasses import dataclass
from datetime import date


@dataclass
class VerifyBankAccountRequest:
    account_number: str
    bank_code: str
    bvn: str


@dataclass
class VerifyBvnRequest:
    bvn: str
    fullname: str
    phone_number: str
    date_of_birth: date
