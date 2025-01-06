# models/app_models.py

from sqlalchemy import create_engine, Column, Integer,Boolean ,String, LargeBinary , Text , Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()





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


class Worker(Base):
    __tablename__ = 'workers'  # Correct table name

    id = Column(Integer, primary_key=True)
    status = Column(String, nullable=True)  # Status
    nummer = Column(String, nullable=False)  # Nummer
    worker = Column(String, nullable=False)  # Worker
    adresse = Column(String, nullable=False)  # Adresse
    plz = Column(String, nullable=False)  # PLZ
    ort = Column(String, nullable=False)  # Ort
    telefon = Column(String, nullable=False)  # Telefon
    mobil = Column(String, nullable=True)  # Mobil (optional)
    email = Column(String, nullable=False)  # E-Mail


    def __repr__(self):
        return f"<Workers(nummer={self.nummer}, worker={self.kunde}, adresse={self.adresse})>"

# Define the new Product model
class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    bild = Column(LargeBinary, nullable=True)  # Image stored as binary data (optional)
    gruppe = Column(String, nullable=True)  # Gruppe (optional)
    nummer = Column(String, nullable=False)  # Nummer (Product number)
    produkt = Column(String, nullable=False)  # Produkt (Product name)
    beschreibung = Column(Text, nullable=True)  # Beschreibung (optional description)
    verkaufspreis = Column(Float, nullable=False)  # Verkaufspreis (Selling price)

    def __repr__(self):
        return f"<Product(nummer={self.nummer}, produkt={self.produkt}, verkaufspreis={self.verkaufspreis})>"



# Define the new Document model
class Document(Base):
    __tablename__ = 'documents'

    id = Column(Integer, primary_key=True)
    status = Column(Boolean, nullable=True)  # Status (optional)
    datum = Column(String, nullable=True)  # Date (optional)
    betreff = Column(String, nullable=False)  # Subject
    kundennummer = Column(String, nullable=False)  # Customer number
    kunde = Column(String, nullable=False)  # Customer
    adresse = Column(String, nullable=False)  # Address
    plz = Column(String, nullable=False)  # Postal code
    ort = Column(String, nullable=False)  # City
    leistungszeitraum = Column(String, nullable=False)  # Service period
    lieferadresse = Column(String, nullable=True)  # Delivery address (optional)
    projekt = Column(String, nullable=True)  # Project (optional)
    summe_netto = Column(Float, nullable=False)  # Net total
    summe_brutto = Column(Float, nullable=False)  # Gross total
    summe_kommentare = Column(Text, nullable=True)  # Comments (optional)
    doc_type = Column(String, nullable=False)  # Document type (e.g., Rechnung, Angebot, Lieferschein)
    
    def __repr__(self):
        return f"<Document(betreff={self.betreff}, kundennummer={self.kundennummer}, summe_netto={self.summe_netto})>"




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





class Nummernvergabe(Base):
    __tablename__ = 'nummernvergabe'

    id = Column(Integer, primary_key=True)
    betreff_angebot = Column(String, nullable=False)  # Betreff Fur Angebot
    nummer_angebot = Column(Integer, nullable=False, default=1)  # Nachste fortlaufende Nummer for Angebot
    betreff_lieferschein = Column(String, nullable=False)  # Betreff Fur Lieferschein
    nummer_lieferschein = Column(Integer, nullable=False, default=1)  # Nachste fortlaufende Nummer for Lieferschein
    betreff_rechnung = Column(String, nullable=False)  # Betreff Fur Rechnung
    nummer_rechnung = Column(Integer, nullable=False, default=1)  # Nachste fortlaufende Nummer for Rechnung


class Anreden(Base):
    __tablename__ = 'anreden'

    id = Column(Integer, primary_key=True)
    gender = Column(String, nullable=False)  # gender


class Einheiten(Base):
    __tablename__ = 'einheiten'

    id = Column(Integer, primary_key=True)
    unit = Column(String, nullable=False)  # unit

class Lander(Base):
    __tablename__ = 'lander'

    id = Column(Integer, primary_key=True)
    land = Column(String, nullable=False)  # country


class Zahlungsarten(Base):
    __tablename__ = 'zahlungsarten'

    id = Column(Integer, primary_key=True)
    payment_method = Column(String, nullable=False)  # country


class billSettings(Base):
    __tablename__ = 'bill_settings'

    id = Column(Integer, primary_key=True)
    currency = Column(String, nullable=False)  # Betreff Fur Angebot
    decimal_places = Column(Integer, nullable=False, default=2)  # Nachste fortlaufende Nummer for Angebot
    prices_is = Column(String, nullable=False)  # Betreff Fur Lieferschein
    VAT = Column(Integer, nullable=False, default=1)  # Nachste fortlaufende Nummer for Lieferschein


# Setup the database connection
engine = create_engine('sqlite:///app.db')  # Or use 'postgresql://user:password@localhost/mydatabase'
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
