cd C:/Project/darknet/x64

./darknet detector test cfg/coco.data cfg/yolov4.cfg yolov4.weights C:/Project/Stereopair/Data/Cam1.jpg -ext_output > C:/Project/Stereopair/Data/Cam1.txt
echo "endstream" >> C:/Project/Stereopair/Data/Cam1.txt 

./darknet detector test cfg/coco.data cfg/yolov4.cfg yolov4.weights C:/Project/Stereopair/Data/Cam2.jpg -ext_output > C:/Project/Stereopair/Data/Cam2.txt
echo "endstream" >> C:/Project/Stereopair/Data/Cam2.txt