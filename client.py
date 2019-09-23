import cv2
import numpy as np

import time

import grpc 
import cas_proto_pb2 as cas_pb2
import cas_proto_pb2_grpc as cas_pb2_grpc

if __name__ == '__main__':

  # camera index
  camera_id = 0

  # setup gRPC connection
  channel = grpc.insecure_channel('localhost:50051')
  stub = cas_pb2_grpc.UploaderStub(channel)

  # setup camera
  cap = cv2.VideoCapture(0)

  for i in range(10):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # encode frame to send via gRPC
    data = cv2.imencode('.jpg', frame)[1].tostring()

    frame_id = str(i).zfill(3)
    meta = "%s-%s" % (camera_id, frame_id)

    # send gRPC request
    print("Sending frame %s from camera %s" % (frame_id, camera_id))
    stub.Upload(cas_pb2.UploadRequest(name = meta, data = data))

    # send frame roughly every 1 sec
    time.sleep(1.0)
