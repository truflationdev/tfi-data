from truflation.data.connector import ConnectorSql
from datetime import datetime
from sqlalchemy import cast, select, String, Float, Integer, Date
from sqlalchemy import Column
from sqlalchemy.orm import declarative_base, Session

# https://stackoverflow.com/questions/33053241/sqlalchemy-if-table-does-not-exist
# https://towardsdatascience.com/the-easiest-way-to-upsert-with-sqlalchemy-9dae87a75c35
Base = declarative_base()
class MetadataTable(Base):
    __tablename__ = '__metadata__'
    table = Column(
        String(256),
        primary_key=True, nullable=False
    )
    key = Column(
        String(256),
        primary_key=True, nullable=False
    )
    valuei = Column(Integer)
    valued = Column(Date)
    valuef = Column(Float)
    values = Column(String(1024))


class Metadata:
    def __init__(self, connect_string):
        self.connector = ConnectorSql(
            connect_string
        )
        Base.metadata.create_all(
            bind=self.connector.engine,
            checkfirst=True
        )

    def write_all(self, table, data):
        with Session(self.connector.engine) as session:
            for k, v in data.items():
                l = None
                if isinstance(v, int):
                    l = MetadataTable(
                        table=table, key=k, valuei=v
                    )
                elif isinstance(v, datetime):
                    l = MetadataTable(
                        table=table, key=k, valued=v
                    )
                elif isinstance(v, float):
                    l = MetadataTable(
                        table=table, key=k, valuef=v
                    )
                elif isinstance(v, str):
                    l = MetadataTable(
                        table=table, key=k, values=v
                    )
                if l is not None:
                    session.merge(l)
            session.commit()

    def read_all(self, table):
        l = {}
        with Session(self.connector.engine) as session:
            stmt = select(MetadataTable).where(
                MetadataTable.table == table
            )
            result = session.execute(stmt)
            for obj in result.scalars().all():
                if obj.valuei is not None:
                    l[obj.key] = obj.valuei
                elif obj.valuef is not None:
                    l[obj.key] = obj.valuef
                elif obj.valued is not None:
                    l[obj.key] = obj.valued
                elif obj.values is not None:
                    l[obj.key] = obj.values
        return l

    def read_by_key(self, key):
        l = {}
        with Session(self.connector.engine) as session:
            stmt = select(MetadataTable).where(
                MetadataTable.key == key
            )
            result = session.execute(stmt)
            for obj in result.scalars().all():
                if obj.valuei is not None:
                    l[obj.table] = obj.valuei
                elif obj.valuef is not None:
                    l[obj.table] = obj.valuef
                elif obj.valued is not None:
                    l[obj.table] = obj.valued
                elif obj.values is not None:
                    l[obj.table] = obj.values
        return l
