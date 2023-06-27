from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

Session = scoped_session(sessionmaker())


def run_app(env=None):
    from app.config import config_by_name
    from app.grpc_server import serve

    config = config_by_name[env or "test"]

    # Configure SQL
    engine = create_engine(config.SQLALCHEMY_DATABASE_URI, echo=config.SQL_ECHO)    
    Session.configure(bind=engine)

    # Start gRPC server
    serve()    
