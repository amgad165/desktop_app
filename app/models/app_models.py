# models/app_models.py

from sqlalchemy import create_engine, Column, Integer, String, LargeBinary , Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class CompanyDetails(Base):
    __tablename__ = 'company_details'

    id = Column(Integer, primary_key=True)
    anrede = Column(String, nullable=False)  # Anrede
    firmenname = Column(String, nullable=False)  # Firmenname
    vorname = Column(String, nullable=False)  # Vorname
    nachname = Column(String, nullable=False)  # Nachname
    adresse = Column(String, nullable=False)  # Adresse
    plz = Column(String, nullable=False)  # PLZ
    ort = Column(String, nullable=False)  # Ort
    land = Column(String, nullable=False)  # Land
    telefon = Column(String, nullable=False)  # Telefon
    fax = Column(String, nullable=True)  # Fax (optional)
    email = Column(String, nullable=False)  # E-Mail
    firmenbuchnummer = Column(String, nullable=False)  # Firmenbuchnummer
    steuernummer = Column(String, nullable=False)  # Steuernummer
    logo_image = Column(LargeBinary, nullable=True)  # Logo image as binary data (optional)

    def __repr__(self):
        return f"<CompanyDetails(firmenname={self.firmenname}, vorname={self.vorname}, nachname={self.nachname})>"



# Define the new Customer model
class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    status = Column(String, nullable=True)  # Status
    nummer = Column(String, nullable=False)  # Nummer
    kunde = Column(String, nullable=False)  # Kunde
    adresse = Column(String, nullable=False)  # Adresse
    plz = Column(String, nullable=False)  # PLZ
    ort = Column(String, nullable=False)  # Ort
    telefon = Column(String, nullable=False)  # Telefon
    mobil = Column(String, nullable=True)  # Mobil (optional)
    email = Column(String, nullable=False)  # E-Mail
    kommentar = Column(Text, nullable=True)  # Kommentar (optional)
    gruppe = Column(String, nullable=True)  # Gruppe (optional)

    def __repr__(self):
        return f"<Customer(nummer={self.nummer}, kunde={self.kunde}, adresse={self.adresse})>"



# Setup the database connection
engine = create_engine('sqlite:///app.db')  # Or use 'postgresql://user:password@localhost/mydatabase'
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
