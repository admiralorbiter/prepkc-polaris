from .base import Base, db
from .address_mixin import AddressMixin
from .contact_mixin import ContactMixin
from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy import Enum

organization_types = ('non-profit', 'government', 'education institution', 'healthcare', 'corporate', 'community org', 'religious', 'research')


class Organization(Base, AddressMixin, ContactMixin):
    __tablename__ = 'organizations'
    id =db.Column(Integer, primary_key=True)
    name =db.Column(String(100), nullable=False, unique=True)
    abbr=db.Column(String(20), nullable=False, unique=True)
    alternative_name = db.Column(String(100))
    org_subgroup = db.Column(String(100))
    type = db.Column(Enum(*organization_types, name='organization_types'), nullable=False)
    email_domain = db.Column(String(100))
    website = db.Column(String(100))
    industry = db.Column(String(100))
    volunteers = relationship('Volunteer', back_populates='primary_affiliation')
    sessions = relationship('Session', secondary='session_organizations_association', back_populates='organizations')
