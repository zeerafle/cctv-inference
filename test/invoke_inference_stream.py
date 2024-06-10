import io
import json
import boto3

# Create a low-level client representing Amazon SageMaker Runtime
sagemaker_runtime = boto3.client("sagemaker-runtime", region_name="ap-southeast-1")
endpoint_name = "cctv-inference"


# Example class that processes an inference stream:
class SmrInferenceStream:

    def __init__(self, sagemaker_runtime, endpoint_name):
        self.sagemaker_runtime = sagemaker_runtime
        self.endpoint_name = endpoint_name
        # A buffered I/O stream to combine the payload parts:
        self.buff = io.BytesIO()
        self.read_pos = 0

    def stream_inference(self, request_body):
        # Gets a streaming inference response
        # from the specified model endpoint:
        response = self.sagemaker_runtime.invoke_endpoint_with_response_stream(
            EndpointName=self.endpoint_name,
            Body=json.dumps(request_body),
            ContentType="application/json",
        )
        # Gets the EventStream object returned by the SDK:
        event_stream = response["Body"]
        for event in event_stream:
            # Passes the contents of each payload part
            # to be concatenated:
            self._write(event["PayloadPart"]["Bytes"])
            # Iterates over lines to parse whole JSON objects:
            for line in self._readlines():
                resp = json.loads(line)
                part = resp.get("outputs")[0]
                # Returns parts incrementally:
                yield part

    # Writes to the buffer to concatenate the contents of the parts:
    def _write(self, content):
        self.buff.seek(0, io.SEEK_END)
        self.buff.write(content)

    # The JSON objects in buffer end with '\n'.
    # This method reads lines to yield a series of JSON objects:
    def _readlines(self):
        self.buff.seek(self.read_pos)
        for line in self.buff.readlines():
            self.read_pos += len(line)
            yield line[:-1]


request_body = {
    "inputs": ["Large model inference is"],
    "parameters": {"max_new_tokens": 100, "enable_sampling": "true"},
}
smr_inference_stream = SmrInferenceStream(sagemaker_runtime, endpoint_name)
stream = smr_inference_stream.stream_inference(request_body)
for part in stream:
    print(part, end="")
