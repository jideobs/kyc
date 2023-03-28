from datasources import register_data_sources
from models import BvnInformation, AccountInformation, DatasourceType, SimRegInformation
from rule import Rule, RulesExecutor

if __name__ == '__main__':
    register_data_sources()

    # Example
    phone_number = '2348091607291'
    bvn = '12345678901'
    account = '2004036157'
    bank_code = '058'
    bank_account_bvn_verification = Rule('check bank account information against BVN information') \
        .fetch(DatasourceType.BVN, bvn) \
        .fetch(DatasourceType.BANK_ACCOUNT, account, bank_code) \
        .where(phone_number == BvnInformation.phone_number) \
        .fuzzy_match(BvnInformation.fullname, AccountInformation.fullname)
    simreg_information_verification = Rule('check SIM registration information against entered data') \
        .fetch(DatasourceType.SIMREG, phone_number) \
        .where(phone_number == SimRegInformation.phone_number) \
        .fuzzy_match(SimRegInformation.fullname, 'Olajide Obasan Bolaji')
    simreg_information_bvn_information = Rule('SIM registration information against BVN information') \
        .fetch(DatasourceType.SIMREG, phone_number) \
        .fetch(DatasourceType.BVN, bvn) \
        .where(phone_number == SimRegInformation.phone_number) \
        .where(SimRegInformation.phone_number == BvnInformation.phone_number) \
        .fuzzy_match(SimRegInformation.fullname, BvnInformation.fullname)

    (RulesExecutor('KYC account users')
     .either(bank_account_bvn_verification)
     .or_(simreg_information_verification)
     .then(simreg_information_bvn_information))

    print(bank_account_bvn_verification)
    print(simreg_information_verification)
    print(simreg_information_bvn_information)
