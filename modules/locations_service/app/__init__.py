import time
import multiprocessing

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

Session = scoped_session(sessionmaker())


def run_app(env=None):    
    from app.config import config_by_name
    from app.grpc_server import serve as gserve
    from app.kafka_server import serve as kserve

    config = config_by_name[env or "test"]

    # Configure SQL
    engine = create_engine(config.SQLALCHEMY_DATABASE_URI, echo=config.SQL_ECHO)    
    Session.configure(bind=engine)

    # Start gRPC and Kafka workers
    workers = []

    print("Starting grpc worker")
    grpc_worker = multiprocessing.Process(target=gserve, args=())
    grpc_worker.start()
    workers.append(grpc_worker)

    print("Starting kafka worker")
    grpc_worker = multiprocessing.Process(target=kserve, args=(config.KAFKA_HOST, config.KAFKA_PORT))
    grpc_worker.start()
    workers.append(grpc_worker)

    print("All workers started")
    for worker in workers:
        worker.join()
    print("All workers finished")
