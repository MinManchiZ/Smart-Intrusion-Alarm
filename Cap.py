import os
import sys
import time
import cv2
import numpy as np

# 添加SDK路径
sdk_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tp_camera", "tplink_v3.6", "tplink")
sys.path.append(sdk_path)

# 设置DLL搜索路径
dll_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tp_camera", "tplink_v3.6", "tplink", "dll")
os.environ['PATH'] = dll_path + os.pathsep + os.environ['PATH']

from tplink.sdk.IPCDevice import IPCDevice
from tplink.sdk.TPOpenNative import SDKReqCallback, TPOpenNative, SDKPlayerCallbackContext
from tplink.sdk.TPSDKContext import TPSDKContext
from tplink.sdk.TPPlayer import TPPlayer
from tplink.sdk.IPCDeviceContext import IPCDeviceContext

class CameraController:
    def __init__(self, ip="172.20.15.100", port=554, username="admin", password="admin"):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.rtsp_url = f"rtsp://{username}:{password}@{ip}:{port}/stream1"
        
        # 初始化SDK上下文
        self.sdk_context = TPSDKContext()
        self.sdk_context.appReqStart(True)  # 同步启动
        
        # 获取设备上下文
        self.dev_context = self.sdk_context.getDevCtx()
        
        # 初始化设备
        self.dev_handle = self.dev_context.initDev(ip, port)
        if self.dev_handle < 0:
            raise Exception("Failed to initialize device")
            
        # 获取设备信息
        self.device = self.dev_context.getDev(self.dev_handle)
        if not self.device:
            raise Exception("Failed to get device info")
            
        # 打印设备信息
        print(f"设备型号: {self.device.getModel()}")
        print(f"视频端口: {self.device.getVideoPort()}")
        
        # 检查是否支持云台
        if not self.device.supportMotor(0, 0):  # 0表示主码流，0表示主通道
            raise Exception("设备不支持云台控制")
            
        # 登录设备
        self._login()
        
        # 初始化视频捕获
        self.cap = cv2.VideoCapture(self.rtsp_url)
        if not self.cap.isOpened():
            raise Exception("Failed to open RTSP stream")
            
    def _login(self):
        """登录设备"""
        def login_callback(req_id, resp, context, user_data):
            if resp.mRval != 0:
                raise Exception(f"Login failed with error code: {resp.mRval}")
                
        # 请求登录
        req_id = self.dev_context.reqLogin(self.dev_handle, login_callback, 0, self.username, self.password)
        if req_id < 0:
            raise Exception("Failed to send login request")
            
        # 等待登录完成
        time.sleep(1)
        
    def move_up(self, speed=5):
        """向上移动"""
        def move_callback(req_id, resp, context, user_data):
            if resp.mRval != 0:
                print(f"Move failed with error code: {resp.mRval}")
                
        # 向上移动，Y坐标减小
        req_id = self.dev_context.reqMotorMoveBy(self.dev_handle, move_callback, 0, 0, -speed)
        if req_id < 0:
            print("Failed to send move request")
            
    def move_down(self, speed=5):
        """向下移动"""
        def move_callback(req_id, resp, context, user_data):
            if resp.mRval != 0:
                print(f"Move failed with error code: {resp.mRval}")
                
        # 向下移动，Y坐标增加
        req_id = self.dev_context.reqMotorMoveBy(self.dev_handle, move_callback, 0, 0, speed)
        if req_id < 0:
            print("Failed to send move request")
            
    def move_left(self, speed=5):
        """向左移动"""
        def move_callback(req_id, resp, context, user_data):
            if resp.mRval != 0:
                print(f"Move failed with error code: {resp.mRval}")
                
        # 向左移动，X坐标减小
        req_id = self.dev_context.reqMotorMoveBy(self.dev_handle, move_callback, 0, -speed, 0)
        if req_id < 0:
            print("Failed to send move request")
            
    def move_right(self, speed=5):
        """向右移动"""
        def move_callback(req_id, resp, context, user_data):
            if resp.mRval != 0:
                print(f"Move failed with error code: {resp.mRval}")
                
        # 向右移动，X坐标增加
        req_id = self.dev_context.reqMotorMoveBy(self.dev_handle, move_callback, 0, speed, 0)
        if req_id < 0:
            print("Failed to send move request")
            
    def move_to(self, x, y):
        """移动到指定坐标"""
        def move_callback(req_id, resp, context, user_data):
            if resp.mRval != 0:
                print(f"Move failed with error code: {resp.mRval}")
                
        # 移动到指定坐标
        req_id = self.dev_context.reqMotorMoveTo(self.dev_handle, move_callback, 0, x, y)
        if req_id < 0:
            print("Failed to send move request")
            
    def zoom_in(self):
        """放大"""
        def zoom_callback(req_id, resp, context, user_data):
            if resp.mRval != 0:
                print(f"Zoom failed with error code: {resp.mRval}")
                
        # 放大，direction=1
        req_id = self.dev_context.reqMotorMoveZoom(self.dev_handle, zoom_callback, 0, 1)
        if req_id < 0:
            print("Failed to send zoom request")
            
    def zoom_out(self):
        """缩小"""
        def zoom_callback(req_id, resp, context, user_data):
            if resp.mRval != 0:
                print(f"Zoom failed with error code: {resp.mRval}")
                
        # 缩小，direction=-1
        req_id = self.dev_context.reqMotorMoveZoom(self.dev_handle, zoom_callback, 0, -1)
        if req_id < 0:
            print("Failed to send zoom request")
            
    def stop(self):
        """停止移动"""
        def stop_callback(req_id, resp, context, user_data):
            if resp.mRval != 0:
                print(f"Stop failed with error code: {resp.mRval}")
                
        # 停止移动
        req_id = self.dev_context.reqMotorMoveStop(self.dev_handle, stop_callback, 0)
        if req_id < 0:
            print("Failed to send stop request")
            
    def get_frame(self):
        """获取当前帧"""
        ret, frame = self.cap.read()
        if not ret:
            return None
        return frame
        
    def cleanup(self):
        """清理资源"""
        if hasattr(self, 'cap'):
            self.cap.release()
        if hasattr(self, 'dev_handle'):
            self.dev_context.destroyDev(self.dev_handle)
        if hasattr(self, 'sdk_context'):
            self.sdk_context.appReqStop(True)

# 使用示例
if __name__ == "__main__":
    try:
        # 创建控制器实例
        camera = CameraController()
        
        # 创建窗口
        cv2.namedWindow("Camera", cv2.WINDOW_NORMAL)
        
        while True:
            # 获取并显示视频帧
            frame = camera.get_frame()
            if frame is not None:
                cv2.imshow("Camera", frame)
            
            # 处理键盘输入
            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # ESC键退出
                break
            elif key == ord('w'):  # W键向上
                camera.move_up()
            elif key == ord('s'):  # S键向下
                camera.move_down()
            elif key == ord('a'):  # A键向左
                camera.move_left()
            elif key == ord('d'):  # D键向右
                camera.move_right()
            elif key == ord('z'):  # Z键放大
                camera.zoom_in()
            elif key == ord('x'):  # X键缩小
                camera.zoom_out()
            elif key == ord(' '):  # 空格键停止
                camera.stop()
                
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        # 清理资源
        if 'camera' in locals():
            camera.cleanup()
        cv2.destroyAllWindows() 