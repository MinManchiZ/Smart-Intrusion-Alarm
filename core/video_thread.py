import cv2
import numpy as np
from PyQt6.QtCore import QThread, pyqtSignal, QTimer

__all__ = ['VideoThread']

class VideoThread(QThread):
    frame_ready = pyqtSignal(np.ndarray)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, source):
        super().__init__()
        self.source = source
        self.running = True
        self.reconnect_timer = QTimer()
        self.reconnect_timer.timeout.connect(self.reconnect)
        self.reconnect_attempts = 0
        self.max_reconnect_attempts = 5
        
    def run(self):
        while self.running:
            try:
                cap = cv2.VideoCapture(self.source)
                if not cap.isOpened():
                    raise Exception("无法打开视频源")
                    
                self.reconnect_attempts = 0
                while self.running:
                    ret, frame = cap.read()
                    if ret:
                        self.frame_ready.emit(frame)
                    else:
                        break
                        
                cap.release()
                if self.running:
                    self.error_occurred.emit("视频流中断，正在重连...")
                    self.reconnect_timer.start(3000)  # 3秒后重试
                    
            except Exception as e:
                self.error_occurred.emit(f"错误: {str(e)}")
                if self.running:
                    self.reconnect_timer.start(3000)
                    
    def reconnect(self):
        self.reconnect_attempts += 1
        if self.reconnect_attempts >= self.max_reconnect_attempts:
            self.error_occurred.emit("重连失败，请检查视频源")
            self.stop()
        else:
            self.start()
            
    def stop(self):
        self.running = False
        self.reconnect_timer.stop()
        self.wait()