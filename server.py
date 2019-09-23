import cv2
import numpy as np

import time
from threading import Thread
from concurrent import futures

import grpc 
import cas_proto_pb2 as cas_pb2
import cas_proto_pb2_grpc as cas_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
MAX_MESSAGE_LENGTH = 1024 * 1024 * 64
MAX_WORKERS = 600

class Uploader(cas_pb2_grpc.UploaderServicer):

  def Upload(self, request, context):
    meta = str(request.name)
    data = request.data

    camera_id, frame_id = meta.split('-')

    # decode frame from gRPC request
    print("Received frame %s from camera %s" % (frame_id, camera_id))
    frame = cv2.imdecode(np.fromstring(data, dtype = np.uint8), -1)

    return cas_pb2.UploadReply(message='OK')

if __name__ == '__main__':
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=MAX_WORKERS), options=[('grpc.max_send_message_length', MAX_MESSAGE_LENGTH), 
                                                                    ('grpc.max_receive_message_length', MAX_MESSAGE_LENGTH),
                                                                    ('grpc.max_message_length', MAX_MESSAGE_LENGTH)])
  cas_pb2_grpc.add_UploaderServicer_to_server(Uploader(), server)
  server.add_insecure_port("localhost:50051")
  server.start()

  try:
    while True:
      time.sleep(_ONE_DAY_IN_SECONDS)
  except KeyboardInterrupt:
    server.stop(0)
