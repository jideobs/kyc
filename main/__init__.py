from datasources import register_data_sources
from models import BvnInformation, AccountInformation, DatasourceType, SimRegInformation
from rule import Rule, RulesExecutor, Either

if __name__ == '__main__':
    register_data_sources()

    # Example
    phone_number = '2348091607291'
    bvn = '12345678901'
    account = '2004036157'
    bank_code = '058'
    check_rule_of_law = Rule('check rule of law') \
        .fetch(DatasourceType.BVN, bvn) \
        .fetch(DatasourceType.BANK_ACCOUNT, account, bank_code) \
        .where(phone_number == BvnInformation.phone_number) \
        .fuzzy_match(BvnInformation.fullname, AccountInformation.fullname)
    check_rule_of_law2 = Rule('check rule of law 2') \
        .fetch(DatasourceType.SIMREG, phone_number) \
        .where(phone_number == SimRegInformation.phone_number)
    check_rule_of_law3 = Rule('check rule of law 3') \
        .fetch(DatasourceType.SIMREG, phone_number) \
        .fetch(DatasourceType.BVN, bvn) \
        .where(phone_number == SimRegInformation.phone_number) \
        .where(SimRegInformation.phone_number == BvnInformation.phone_number) \
        .fuzzy_match(SimRegInformation.fullname, BvnInformation.fullname)

    (RulesExecutor('')
     .either(check_rule_of_law)
     .or_(check_rule_of_law2)
     .then(check_rule_of_law3))

    print(check_rule_of_law)
    print(check_rule_of_law2)
    print(check_rule_of_law3)
