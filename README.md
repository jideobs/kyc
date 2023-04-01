# KYC Service

With the never-ending verification and validation of customers within the fintech space, you would definitely need multiple sources of data on customers whether it's for the phone number, BVN, bank account number, or NIN provided you would need to verify the customer against these data sources.

There are multiple problems commonly encountered when a Fintech is trying to validate such customers, some are:

- Integrating and managing multiple data sources for all data points being verified or validated.
- Writing, testing, and maintaining custom verification/validation conditions based on the needs of the Fintech company.

## **Goal**

To circumvent these problems it then decided that there should be a KYC service that allows for the integration of different data sources available out there as third parties, which are then integrated under the umbrella of different data-id types. Another part of the system would allow the software engineer to write intuitive rules which are easier to read and maintain for different verification/validation scenarios. This means a DSL is provided which allows the software engineers/any technical persons to write these rules.

## Requirements

- The system shall allow one to integrate data sources easily by providing such configurations so the system could in turn query for data with respect to a data ID.
- The system shall allow one to write named rules to give the ability to carry out validations/verifications based on data sources for its customers/users, which returns a useful result of the validation/verification for further analysis or decision-making.
- The system shall expose these rules via an HTTP endpoint for requests of customer/user validations/verifications.

## Designs

**Datasource**

To provide somewhat a solution to the above-stated problems we have decided to identify different data types which are customer/user information attached to a particular ID or unique identifier, some of which are: 

- BVN
- NIN
- Bank account number
- Phone number

With these, we now have different data sources(Third party clients that offer this data via API calls) which then provide personal information with respect to the IDs. Within our system/service 

we now have ******BvnInformation, BankAccountInformation, NINInformation, PhoneNumberInformation******.

It is also paramount to know that we also provide integration to multiple data sources offering the same information types just for resilience and tolerance.

**Rule**

To combat the problem of complicated code, maintenance, ease of test, and truth with KYC especially fraud since without a simple way of writing conditions for verifying/validating customers/users it's easy to make mistakes and difficult to make mistakes. The solution here is to provide an internal DSL where its easy to write rules that makes use of data from the data sources, these rules are intuitive to anyone within the company that sees them:

```python
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
```

There are 3 rules above which are either written to compare data from its sources against raw inputted data or data from one source against another. This would ensure the flexibility required to write new KYC rules, change them, test, or know the current state of KYC in the system.

******************Rule Executors******************

This would be used to combine/execute rules from above, depending on the situation we might want to combine different rules or have fallback rules in-case the previous failed.

```python
kyc_account_verification = RulesExecutor('KYC account users') \
        .either([bank_account_bvn_verification, simreg_information_verification]) \
        .or_([simreg_information_bvn_information]) \
        .execute()
```

This example combines the first 2 rules which must pass or execute the last rule, the result can then be used to make decisions.

The diagram below should better illustrate the intention of the code architecture for this proposed KYC service.

![Untitled](KYC%20Service%20700d814e74de45e6a12304a65c88aca7/Untitled.png)