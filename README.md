# YOLOv7-ONNX-RKNN-Detection
***Remark: This repo only support 1 batch size***
![!YOLOv7 ONNX RKNN Detection Picture](https://github.com/laitathei/YOLOv7-ONNX-RKNN-Detection/blob/main/doc/visual_image.jpg)
![!YOLOv7 ONNX RKNN Detection Video](https://github.com/laitathei/YOLOv7-ONNX-RKNN-Detection/blob/main/doc/result.gif)

Video source: https://www.youtube.com/watch?v=n3Dru5y3ROc&t=0s
```
git clone --recursive https://github.com/laitathei/YOLOv7-ONNX-RKNN-HORIZON-Detection.git
```
## 0. Environment Setting
```
torch: 1.10.1+cu102
torchvision: 0.11.2+cu102
onnx: 1.10.0
onnxruntime: 1.10.0
```

## 1. Yolov7 Prerequisite
```
cd yolov7
pip3 install -r requirements.txt
```

## 2. Convert Pytorch model to ONNX
Remember to change the variable to your setting.
```
python3 pytorch2onnx.py --weights ./model/yolov7-tiny.pt --simplify --img-size 480 640 --max-wh 640 --topk-all 100 --end2end --grid
```

## 3. RKNN Prerequisite
Install the wheel according to your python version
```
cd rknn-toolkit2/packages
pip3 install rknn_toolkit2-1.5.0+1fa95b5c-cpxx-cpxx-linux_x86_64.whl
```

## 4. Modify ONNX network structure
Install ONNX modifier and start flask service
```
cd onnx-modifier
pip3 install -r requirements.txt
pip3 install onnx==1.10.0
python3 app.py
```

Enter ```http://127.0.0.1:5000/```
Cut the below part of the network
![!YOLOv7 ONNX RKNN Detection Picture 1](https://github.com/laitathei/YOLOv7-ONNX-RKNN-Detection/blob/main/doc/step2.jpeg)

Add the new output and download it
![!YOLOv7 ONNX RKNN Detection Picture 2](https://github.com/laitathei/YOLOv7-ONNX-RKNN-Detection/blob/main/doc/step1.jpeg)

Move the modified newtork to replace the old one
```
mv ./onnx-modifier/modified_onnx/modified_{model_name}-{input_height}-{input_width}.onnx ./model/{model_name}-{input_height}-{input_width}.onnx
```

## 5. Convert ONNX model to RKNN
Remember to change the variable to your setting
To improve perfermance, you can change ```./config/yolov7-seg-xxx-xxx.quantization.cfg``` layer type.
Please follow [official document](https://github.com/rockchip-linux/rknn-toolkit2/blob/master/doc/Rockchip_User_Guide_RKNN_Toolkit2_EN-1.5.0.pdf) hybrid quatization part and reference to [example program](https://github.com/rockchip-linux/rknn-toolkit2/tree/master/examples/functions/hybrid_quant) to modify your codes.
```
python3 onnx2rknn_step1.py
python3 onnx2rknn_step2.py
```

## 6. RKNN-Lite Inference
```
python3 rknn_lite_inference.py
```

## 7. Horizon Prerequisite
```
wget -c ftp://xj3ftp@vrftp.horizon.ai/ai_toolchain/ai_toolchain.tar.gz --ftp-password=xj3ftp@123$%
tar -xvf ai_toolchain.tar.gz
cd ai_toolchain/
pip3 install h*
```

## 7. Convert ONNX model to Horizon
get onnx file with ```opset 11```
```
python3 pytorch2onnx.py --weights ./model/yolov7-tiny.pt --simplify --img-size 480 640 --max-wh 640 --topk-all 100 --end2end --grid --opset 11
```
Follow ```Step 4``` to delete part of model, and run ```remove_value_list.py``` to remove corresponding value in model
Remember to change the variable to your setting include ```yolov7det_config.yaml```
```
sh 01_check.sh
sh 02_preprocess.sh
sh 03_build.sh
```

## 8. Horizon Inference
```
python3 horizion_simulator_inference.py
python3 horizion_onboard_inference.py
```

## 9. Onnx Runtime Inference
```
python3 onnxruntime_inference.py
```

## Reference
```
https://blog.csdn.net/magic_ll/article/details/131944207
https://github.com/ibaiGorordo/ONNX-YOLOv8-Instance-Segmentation
```
