from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import Column, String

class NameMixin:
    @declared_attr
    def salutation(cls):
        return Column(String(20))

    @declared_attr
    def nickname(cls):
        return Column(String(50))

    @declared_attr
    def first_name(cls):
        return Column(String(50))

    @declared_attr
    def last_name(cls):
        return Column(String(50))

    @declared_attr
    def middle_name(cls):
        return Column(String(50))

    @declared_attr
    def suffix(cls):
        return Column(String(20))
