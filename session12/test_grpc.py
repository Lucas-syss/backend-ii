"""Quick integration test for both gRPC services."""
import subprocess
import sys
import time
import grpc
import cube_pb2
import cube_pb2_grpc
import stream_pb2
import stream_pb2_grpc


def test_cube_service():
    print("=== Testing CubeService (exercise) ===")
    srv = subprocess.Popen(
        [sys.executable, "exercise_server.py"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    time.sleep(1.5)
    try:
        channel = grpc.insecure_channel("localhost:50051")
        stub = cube_pb2_grpc.CubeServiceStub(channel)
        for number in [2, 3, -4, 0.5, 10]:
            reply = stub.ComputeCube(cube_pb2.CubeRequest(number=number))
            expected = number ** 3
            status = "OK" if abs(reply.result - expected) < 1e-9 else "FAIL"
            print(f"  [{status}] cube({number}) = {reply.result}")
    finally:
        srv.terminate()


def test_counter_service():
    print("\n=== Testing CounterService (challenge) ===")
    srv = subprocess.Popen(
        [sys.executable, "challenge_server.py"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    time.sleep(1.5)
    try:
        channel = grpc.insecure_channel("localhost:50052")
        stub = stream_pb2_grpc.CounterServiceStub(channel)
        print("  Counting to 50 in 5 steps:")
        for reply in stub.CountUp(stream_pb2.CountRequest(number=50, steps=5)):
            print(f"    Step {reply.step}: {reply.value}")
    finally:
        srv.terminate()


if __name__ == "__main__":
    test_cube_service()
    test_counter_service()
    print("\nAll tests passed.")
