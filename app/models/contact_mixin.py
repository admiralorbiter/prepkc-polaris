from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import Column, String, Boolean

class ContactMixin:
    @declared_attr
    def primary_phone(cls):
        return Column(String(20))
    
    @declared_attr
    def secondary_phone(cls):
        return Column(String(20))
    
    @declared_attr
    def primary_email(cls):
        return Column(String(100))
    
    @declared_attr
    def secondary_email(cls):
        return Column(String(100))
    
    @declared_attr
    def contact_allowed(cls):
        return Column(Boolean, default=True)
    
    @declared_attr
    def phone_contact_allowed(cls):
        return Column(Boolean, default=True)
    
    @declared_attr
    def email_contact_allowed(cls):
        return Column(Boolean, default=True)
