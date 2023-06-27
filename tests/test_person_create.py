import os
import grpc
import udaconnect_pb2
import udaconnect_pb2_grpc

from dotenv import load_dotenv

load_dotenv()
GRPC_PERSON_HOSTPORT = os.environ["GRPC_PERSON_HOSTPORT"]

channel = grpc.insecure_channel(GRPC_PERSON_HOSTPORT)
stub = udaconnect_pb2_grpc.PersonServiceStub(channel)

# Update this with desired payload
person = udaconnect_pb2.PersonMessage(
    id=2222,
    first_name="Chuck",    
    last_name='Yeager',
    company_name='USAF'
)

response = stub.Create(person)
print(response)