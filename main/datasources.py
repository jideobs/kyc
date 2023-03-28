from typing import List, Any

from uplink import Consumer

from clients import Okra, Nibss, Appzone
from models import BvnInformation, AccountInformation, DatasourceType, SimRegInformation


class Datasource:
    def __init__(self, http_clients: List[Consumer]):
        self.http_clients = http_clients

    def get(self, *_input: Any) -> Any:
        raise NotImplemented


class Bvn(Datasource):
    def get(self, bvn: str) -> BvnInformation:
        return BvnInformation(
            bvn='12345678901',
            first_name='Olajide',
            last_name='Obasan',
            phone_number='2348091607293',
            fullname='Olajide Bolaji Obasan')


class BankAccount(Datasource):
    def get(self, account_no: str, bank_code: str) -> AccountInformation:
        return AccountInformation(
            account_number=account_no,
            first_name='Olajide',
            last_name='Obasan',
            phone_number='2348091607291',
            fullname='Obasan Bolaji Olajide')


class Nin(Datasource):
    def get(self, nin: str):
        pass


class SIMReg(Datasource):
    def get(self, phone_number: str) -> SimRegInformation:
        return SimRegInformation(
            first_name='Olajide',
            last_name='Obasan',
            phone_number='2348091607293',
            fullname='Olajide Bolaji Obasan'
        )


class DatasourceFactory:
    def __init__(self):
        self._data_sources = {}

    def register_datasource(self, name: DatasourceType, datasource: Datasource) -> None:
        self._data_sources[name] = datasource

    def get_datasource(self, name: DatasourceType) -> Datasource:
        data_source = self._data_sources.get(name)
        if not data_source:
            raise ValueError(name)
        return data_source


datasource_factory = DatasourceFactory()


def register_data_sources():
    okra_client = Okra(url='https://api.okra.ng/v2')
    nibss_client = Nibss(url='https://nibss.com')
    appzone_client = Appzone(url='https://appzone.com/')

    datasource_factory.register_datasource(
        DatasourceType.BVN, Bvn(http_clients=[okra_client, nibss_client, appzone_client]))
    datasource_factory.register_datasource(
        DatasourceType.BANK_ACCOUNT, BankAccount(http_clients=[okra_client]))
    datasource_factory.register_datasource(
        DatasourceType.SIMREG, Bvn(http_clients=[okra_client]))
