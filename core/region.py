import cv2

class Region:
    def __init__(self, name):
        self.name = name
        self.points = []
        self.max_points = 6
        self.is_complete = False
        
    def add_point(self, point):
        if len(self.points) < self.max_points:
            self.points.append(point)
            if len(self.points) >= 3:
                self.is_complete = True
            return True
        return False
        
    def draw(self, frame):
        if len(self.points) < 2:
            return frame
            
        # 绘制已连接的点
        for i in range(len(self.points) - 1):
            cv2.line(frame, self.points[i], self.points[i + 1], (0, 255, 0), 2)
            
        # 如果区域完成，连接首尾点
        if self.is_complete:
            cv2.line(frame, self.points[-1], self.points[0], (0, 255, 0), 2)
            
        # 绘制所有点
        for point in self.points:
            cv2.circle(frame, point, 5, (0, 0, 255), -1)
            
        # 显示区域名称和点数
        if self.points:
            text = f"{self.name}: {len(self.points)}/{self.max_points}点"
            cv2.putText(frame, text, (self.points[0][0], self.points[0][1] - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            
        return frame 