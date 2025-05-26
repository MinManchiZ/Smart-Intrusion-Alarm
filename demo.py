import tkinter as tk
from pytapo import Tapo

class CameraController:
    def __init__(self, ip, username, password):
        self.cam = Tapo(ip, username, password)

    def move_camera(self, direction):
        if direction == 'up':
            self.cam.move_up()
        elif direction == 'down':
            self.cam.move_down()
        elif direction == 'left':
            self.cam.move_left()
        elif direction == 'right':
            self.cam.move_right()
        elif direction == 'stop':
            self.cam.stop_move()
        else:
            print("未知方向")

class CameraControlUI:
    def __init__(self, master, controller):
        self.controller = controller
        self.master = master
        master.title("TP-Link 摄像头控制")

        # 上下左右按钮
        tk.Button(master, text="↑", width=10, height=2,
                  command=lambda: self.move("up")).grid(row=0, column=1)

        tk.Button(master, text="←", width=10, height=2,
                  command=lambda: self.move("left")).grid(row=1, column=0)

        tk.Button(master, text="→", width=10, height=2,
                  command=lambda: self.move("right")).grid(row=1, column=2)

        tk.Button(master, text="↓", width=10, height=2,
                  command=lambda: self.move("down")).grid(row=2, column=1)

        tk.Button(master, text="停止", width=10, height=2,
                  command=lambda: self.move("stop")).grid(row=1, column=1)

    def move(self, direction):
        self.controller.move_camera(direction)

if __name__ == "__main__":
    # 替换为你的摄像头信息
    camera_ip = "172.20.15.100:553"
    username = "admin"
    password = "admin"

    controller = CameraController(camera_ip, username, password)

    root = tk.Tk()
    app = CameraControlUI(root, controller)
    root.mainloop()
