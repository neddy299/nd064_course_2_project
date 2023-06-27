import os
import grpc
import udaconnect_pb2
import udaconnect_pb2_grpc

from dotenv import load_dotenv

load_dotenv()
GRPC_PERSON_HOSTPORT = os.environ["GRPC_PERSON_HOSTPORT"]

channel = grpc.insecure_channel(GRPC_PERSON_HOSTPORT)
stub = udaconnect_pb2_grpc.PersonServiceStub(channel)

print("Retrieve one")
response = stub.Retrieve(udaconnect_pb2.PersonRequest(id=1))
print(response)

print("Retrieve All")
response = stub.RetrieveAll(udaconnect_pb2.Empty())
print(response)
