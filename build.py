import PyInstaller.__main__
import os

# 获取当前目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 定义需要打包的文件和资源
PyInstaller.__main__.run([
    'demo2.py',  # 主程序文件
    '--name=区域检测系统',  # 生成的exe名称
    '--windowed',  # 使用GUI模式
    '--onefile',  # 打包成单个exe文件
    '--clean',  # 清理临时文件
    '--add-data=yolov8l.pt;.',  # 添加YOLO模型文件
    '--icon=icon.ico',  # 如果有图标文件的话
    '--noconfirm',  # 不询问确认
    '--hidden-import=torch',
    '--hidden-import=torchvision',
    '--hidden-import=ultralytics',
    '--hidden-import=cv2',
    '--hidden-import=numpy',
]) 