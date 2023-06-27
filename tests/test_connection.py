import os
import grpc
import udaconnect_pb2
import udaconnect_pb2_grpc

from dotenv import load_dotenv

load_dotenv()
GRPC_PERSON_HOSTPORT = os.environ["GRPC_PERSON_HOSTPORT"]

channel = grpc.insecure_channel(GRPC_PERSON_HOSTPORT)
stub = udaconnect_pb2_grpc.ConnectionServiceStub(channel)

print("Retrieve connection")
response = stub.FindContacts(udaconnect_pb2.ConnectionRequest(id="5", start_date="2020-01-01", end_date="2020-12-30", distance="5"))
print(response)
