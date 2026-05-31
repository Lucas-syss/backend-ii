import grpc
import stream_pb2
import stream_pb2_grpc


def run():
    with grpc.insecure_channel("localhost:50052") as channel:
        stub = stream_pb2_grpc.CounterServiceStub(channel)

        print("Counting from 0 to 100 in 5 steps:")
        for reply in stub.CountUp(stream_pb2.CountRequest(number=100, steps=5)):
            print(f"  Step {reply.step}: {reply.value}")

        print("\nCounting from 0 to 1 in 10 steps:")
        for reply in stub.CountUp(stream_pb2.CountRequest(number=1, steps=10)):
            print(f"  Step {reply.step}: {reply.value}")


if __name__ == "__main__":
    run()
