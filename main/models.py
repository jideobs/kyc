from enum import Enum

from descriptors import Field


class DatasourceType(Enum):
    BVN = 1
    NIN = 2
    SIMREG = 3
    BANK_ACCOUNT = 4


class Base:
    def __init__(self, **kwargs):
        super().__init__()
        for key, value in kwargs.items():
            self.__dict__[key] = value

    def __str__(self) -> str:
        s = ''
        for key, value in self.__dict__.items():
            s += f'{key}: {value} '
        return s


class BvnInformation(Base):
    type_ = DatasourceType.BVN

    bvn = Field()
    first_name = Field()
    last_name = Field()
    phone_number = Field()
    fullname = Field()


class AccountInformation(Base):
    type_ = DatasourceType.BANK_ACCOUNT

    account_number = Field()
    bvn = Field()
    first_name = Field()
    last_name = Field()
    fullname = Field()
    phone_number = Field()


class NinInformation(Base):
    type_ = DatasourceType.NIN

    nin = Field()
    first_name = Field()
    last_name = Field()
    phone_number = Field()


class SimRegInformation(Base):
    type_ = DatasourceType.SIMREG

    phone_number = Field()
    first_name = Field()
    last_name = Field()
    fullname = Field()


class ProvidedInput(Base):
    bvn = Field()
    phone_number = Field()
    account_number = Field()
    bank_code = Field()
    first_name = Field()
    last_name = Field()
    middle_name = Field()
    fullname = Field()
    gender = Field()
    date_of_birth = Field()
