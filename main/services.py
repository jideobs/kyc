from main.request import VerifyBankAccountRequest, VerifyBvnRequest


class KycService:
    async def verify_account_information(self, verify_bank_account_request: VerifyBankAccountRequest):
        pass

    async def verify_wallet_account_information(self, verify_bank_account_request: VerifyBankAccountRequest):
        pass

    async def verify_bvn(self, verify_bvn_request: VerifyBvnRequest):
        pass
