import time
from concurrent import futures

import grpc
import udaconnect_pb2_grpc
from app.udaconnect.controllers import ConnectionServicer, PersonServicer


def serve():
    # Initialize gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    udaconnect_pb2_grpc.add_PersonServiceServicer_to_server(PersonServicer(), server)
    udaconnect_pb2_grpc.add_ConnectionServiceServicer_to_server(ConnectionServicer(), server)

    # TODO: move port number to configuration
    print("Server gRPC starting on port 5005...")
    server.add_insecure_port("[::]:5005")
    server.start()
    #Keep thread alive
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

