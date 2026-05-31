from concurrent import futures
import grpc
import stream_pb2
import stream_pb2_grpc


class CounterServicer(stream_pb2_grpc.CounterServiceServicer):
    """Streams intermediate values from 0 up to number, in `steps` increments."""

    def CountUp(self, request, context):
        total = request.number
        steps = max(1, request.steps)
        increment = total / steps

        for i in range(1, steps + 1):
            value = round(increment * i, 6)
            print(f"  Streaming step {i}/{steps}: {value}")
            yield stream_pb2.CountReply(value=value, step=i)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    stream_pb2_grpc.add_CounterServiceServicer_to_server(CounterServicer(), server)
    server.add_insecure_port("[::]:50052")
    server.start()
    print("Streaming server listening on port 50052 ...")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
