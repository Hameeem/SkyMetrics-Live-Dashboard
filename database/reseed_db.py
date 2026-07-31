import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import engine, Base
from database.seed_data import seed_database

def reseed():
    print("Resetting data warehouse and re-seeding with updated Indian flight routes...")
    Base.metadata.drop_all(bind=engine)
    seed_database()

if __name__ == "__main__":
    reseed()
