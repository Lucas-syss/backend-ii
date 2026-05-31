import grpc
import cube_pb2
import cube_pb2_grpc


def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = cube_pb2_grpc.CubeServiceStub(channel)

        for number in [2, 3, -4, 0.5, 10]:
            response = stub.ComputeCube(cube_pb2.CubeRequest(number=number))
            print(f"Cube of {number} = {response.result}")


if __name__ == "__main__":
    run()
