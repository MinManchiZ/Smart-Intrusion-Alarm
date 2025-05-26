import time
import cv2
import numpy as np
from ultralytics import YOLO
from newland_api import NewlandApiClient

# 初始化模型
model = YOLO("yolov8l.pt")

# 初始化摄像头
rtsp_url = "rtsp://admin:admin@172.20.15.100:554/stream1"
cap = cv2.VideoCapture(rtsp_url)

# 初始化新大陆 API 客户端
client = NewlandApiClient("15264831195", "zzh20250716")
client.login()

# 区域设置
drawing = False
current_pts = []
roi_list = []

def draw_roi(event, x, y, flags, param):
    global drawing, current_pts, roi_list
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        current_pts = [(x, y)]
    elif event == cv2.EVENT_MOUSEMOVE and drawing:
        if len(current_pts) == 1:
            current_pts.append((x, y))
        else:
            current_pts[1] = (x, y)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        if len(current_pts) == 2:
            x1, y1 = current_pts[0]
            x2, y2 = current_pts[1]
            roi_polygon = [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]
            roi_list.append(roi_polygon)
            current_pts = []

def is_inside(p, region):
    return cv2.pointPolygonTest(np.array(region, dtype=np.int32), p, False) >= 0

cv2.namedWindow("frame", cv2.WINDOW_NORMAL)  # 可变窗口大小
cv2.setMouseCallback("frame", draw_roi)

# 状态变量
alarm_on = False
last_seen_time = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    now = time.time()
    someone_inside = False

    # 绘制所有 ROI 区域
    for roi in roi_list:
        cv2.polylines(frame, [np.array(roi)], isClosed=True, color=(0, 255, 0), thickness=2)

    # 绘制当前正在绘制的区域
    if len(current_pts) == 2:
        x1, y1 = current_pts[0]
        x2, y2 = current_pts[1]
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 0), 2)

    # 检测人
    results = model(frame, classes=[0])
    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

            for roi in roi_list:
                if is_inside((cx, cy), roi):
                    someone_inside = True
                    last_seen_time = now
                    cv2.putText(frame, "Person IN REGION", (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    break

    # 控制逻辑
    if someone_inside and not alarm_on:
        print("⚠️ 有人进入区域，开启报警")
        client.send_command("1226581", "Waring_1", 1)
        alarm_on = True
    elif not someone_inside and alarm_on and (now - last_seen_time) > 2:
        print("✅ 人员离开区域，关闭报警")
        client.send_command("1226581", "Waring_1", 0)
        alarm_on = False

    # 自适应窗口缩放图像显示
    win_w, win_h = cv2.getWindowImageRect("frame")[2:]
    resized_frame = cv2.resize(frame, (win_w, win_h))
    cv2.imshow("frame", resized_frame)

    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # ESC 退出
        break
    elif key == ord('c'):  # 清除所有区域
        print("🧹 清除所有区域")
        roi_list.clear()
    elif key == ord('z'):  # 撤销上一个区域
        if roi_list:
            roi_list.pop()
            print("↩️ 撤销最近一个区域")

cap.release()
cv2.destroyAllWindows()
