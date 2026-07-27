
from sqlmodel import create_engine

sqlite_file_name ="tasks.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# check_same_thread=False is unique and required for SQLite
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

