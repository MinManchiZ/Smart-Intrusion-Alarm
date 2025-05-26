import sys
import requests

class NewlandApiClient:
    def __init__(self, account, password):
        self.account = account 
        self.password = password  
        self.access_token = None 

    # 登录方法，使用账号和密码登录新大陆云平台
    def login(self):
        try:
            response = requests.post("http://api.nlecloud.com/Users/Login", json={
                "Account": self.account, "Password": self.password, "IsRememberMe": False})
            if response.status_code == 200 and response.json().get("Status") == 0:
                self.access_token = response.json()["ResultObj"]["AccessToken"]  
                return True
        except Exception as e:
            pass 
        return False  # 登录失败返回False

    # 发送命令方法，用于控制设备
    def send_command(self, device_id, api_tag, value):
        if self.access_token:  # 如果有访问令牌
            try:
                response = requests.post("http://api.nlecloud.com/Cmds", json=value, params={
                    "deviceId": device_id, "apiTag": api_tag}, headers={'AccessToken': self.access_token})
            except Exception as e:
                pass

# 程序入口点
if __name__ == "__main__":
    account, password, device_id = "", "", ""  # 设置账号、密码和设备ID
    client = NewlandApiClient(account, password)  # 创建新大陆客户端实例

    if client.login():  # 如果登录成功
        while True:
            user_input = input("输入 '1' 开灯, '0' 关灯 (其他退出): ")
            if user_input == '1':
                client.send_command(device_id, "Waring_1", 1)  # 发送开灯命令
            elif user_input == '0':
                client.send_command(device_id, "Waring_1", 0)  # 发送关灯命令
            else:
                break
    # else: # Removed
        # print("无法登录，程序退出") # Removed

