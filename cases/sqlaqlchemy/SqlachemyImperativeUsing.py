# nuitka-project: --standalone
from sqlalchemy import Column, ForeignKey, Integer, String, Table, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


if __name__ == "__main__":
    metadata = MetaData()

    Person = Table(
        "person",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("name", String(250), nullable=False),
    )

    Address = Table(
        "address",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("street_name", String(250)),
        Column("street_number", String(250)),
        Column("post_code", String(250), nullable=False),
        Column("person_id", Integer, ForeignKey("person.id")),
    )

    # Create an engine that stores data in the local directory's
    # sqlalchemy_example.db file.
    engine = create_engine("sqlite://")

    # Create all tables in the engine. This is equivalent to "Create Table"
    # statements in raw SQL.
    metadata.create_all(engine)

    # Bind the engine to the metadata of the Base class so that the
    # declaratives can be accessed through a DBSession instance
    metadata.bind = engine

    DBSession = sessionmaker(bind=engine)
    # A DBSession() instance establishes all conversations with the database
    # and represents a "staging zone" for all the objects loaded into the
    # database session object. Any change made against the objects in the
    # session won't be persisted into the database until you call
    # session.commit(). If you're not happy about the changes, you can
    # revert all of them back to the last commit by calling
    # session.rollback()
    session = DBSession()

    # Insert a Person in the person table
    new_person = Person.insert().values(name="John Doe")
    session.execute(new_person)
    session.commit()

    # Insert an Address in the address table
    new_address = Address.insert().values(
        street_name="Main Street", street_number="123", post_code="12345", person_id=1
    )
    session.execute(new_address)
    session.commit()

    # Query the database to retrieve the person and address
    person_result = session.execute(Person.select()).fetchall()
    address_result = session.execute(Address.select()).fetchall()

    print("Persons:", person_result)
    print("Addresses:", address_result)
