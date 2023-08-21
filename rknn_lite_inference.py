import os, cv2, time, numpy as np
from util import *
from rknnlite.api import RKNNLite

conf_thres = 0.25
iou_thres = 0.45
input_width = 640
input_height = 480
model_name = 'yolov7-tiny'
model_path = "./model"
config_path = "./config"
result_path = "./result"
image_path = "./dataset/bus.jpg"
video_path = "test.mp4"
video_inference = True
RKNN_MODEL = f'{model_path}/{model_name}-{input_height}-{input_width}.rknn'
CLASSES = ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis','snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush']

if __name__ == '__main__':
    isExist = os.path.exists(result_path)
    if not isExist:
        os.makedirs(result_path)
    rknn_lite = RKNNLite(verbose=False)
    ret = rknn_lite.load_rknn(RKNN_MODEL)
    ret = rknn_lite.init_runtime()
    
    if video_inference == True:
        cap = cv2.VideoCapture(video_path)
        size = (640, 480)
        result = cv2.VideoWriter('result.mp4', cv2.VideoWriter_fourcc('m','p','4','v'), 10, size)
        while(True):
            ret, image_3c = cap.read()
            if not ret:
                break
            print('--> Running model for video inference')
            image_4c, image_3c = preprocess(image_3c, input_height, input_width)
            outputs = rknn_lite.inference(inputs=[image_3c])
            outputs[0] = np.squeeze(outputs[0])
            outputs[0] = np.expand_dims(outputs[0], axis=0)
            colorlist = gen_color(len(CLASSES))
            results = postprocess(outputs, image_4c, image_3c, conf_thres, iou_thres) ##[box,mask,shape]
            results = results[0]              ## batch=1
            boxes, shape = results
            if isinstance(boxes, np.ndarray):
                vis_img = vis_result(image_3c, results, colorlist, CLASSES, result_path)
                cv2.imshow("vis_img", vis_img)
                result.write(vis_img)
            else:
                print("No detection result")
            cv2.waitKey(1)
    else:
        image_3c = cv2.imread(image_path)
        image_4c, image_3c = preprocess(image_3c, input_height, input_width)
        outputs = rknn_lite.inference(inputs=[image_3c])
        outputs[0] = np.squeeze(outputs[0])
        outputs[0] = np.expand_dims(outputs[0], axis=0)
        colorlist = gen_color(len(CLASSES))
        results = postprocess(outputs, image_4c, image_3c, conf_thres, iou_thres) ##[box,mask,shape]
        results = results[0]              ## batch=1
        boxes, shape = results
        if isinstance(boxes, np.ndarray):
            vis_img = vis_result(image_3c, results, colorlist, CLASSES, result_path)
            print('--> Save inference result')
        else:
            print("No detection result")

    print("RKNN inference finish")
    rknn_lite.release()
    cv2.destroyAllWindows()
