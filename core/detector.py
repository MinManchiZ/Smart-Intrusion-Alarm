import cv2
import numpy as np
from ultralytics import YOLO
import torch

class Detector:
    def __init__(self):
        # 检查CUDA是否可用
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print(f"使用设备: {self.device}")
        
        # 加载YOLO模型
        self.model = YOLO("yolov8l.pt")
        self.model.to(self.device)
        
        # 设置检测参数
        self.conf_threshold = 0.5
        self.class_ids = [0]  # 只检测人
        
    def detect(self, frame):
        # 执行检测
        results = self.model(frame, conf=self.conf_threshold, classes=self.class_ids)
        
        # 获取检测结果
        detections = []
        for result in results:
            boxes = result.boxes
            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = float(box.conf[0])
                detections.append({
                    'bbox': (x1, y1, x2, y2),
                    'confidence': conf
                })
                
        return detections
        
    def draw_detections(self, frame, detections):
        for det in detections:
            x1, y1, x2, y2 = det['bbox']
            conf = det['confidence']
            
            # 绘制边界框
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            # 绘制置信度
            text = f"人: {conf:.2f}"
            cv2.putText(frame, text, (x1, y1 - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                       
        return frame
        
    def check_region_invasion(self, detections, regions):
        invasions = []
        for det in detections:
            x1, y1, x2, y2 = det['bbox']
            center = ((x1 + x2) // 2, (y1 + y2) // 2)
            
            for region in regions:
                if region.is_complete:
                    # 检查中心点是否在区域内
                    if self._is_point_in_polygon(center, region.points):
                        invasions.append({
                            'detection': det,
                            'region': region
                        })
                        
        return invasions
        
    def _is_point_in_polygon(self, point, polygon):
        return cv2.pointPolygonTest(np.array(polygon, dtype=np.int32), point, False) >= 0 