from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import Column, String

class AddressMixin:
    @declared_attr
    def city(cls):
        return Column(String(100))

    @declared_attr
    def state(cls):
        return Column(String(100))

    @declared_attr
    def street(cls):
        return Column(String(200))

    @declared_attr
    def zipcode(cls):
        return Column(String(20))

    @declared_attr
    def country(cls):
        return Column(String(100))

    @declared_attr
    def state_code(cls):
        return Column(String(10))

    @declared_attr
    def country_code(cls):
        return Column(String(10))
