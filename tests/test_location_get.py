import os
import grpc
import udaconnect_pb2
import udaconnect_pb2_grpc

from dotenv import load_dotenv

load_dotenv()
GRPC_LOCATION_HOSTPORT = os.environ["GRPC_LOCATION_HOSTPORT"]

channel = grpc.insecure_channel(GRPC_LOCATION_HOSTPORT)
stub = udaconnect_pb2_grpc.LocationServiceStub(channel)

print("Retrieve location")
response = stub.Retrieve(udaconnect_pb2.LocationRequest(id=42))
print(response)
