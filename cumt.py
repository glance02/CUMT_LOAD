import sys
import os
import time
import json
import requests
import re
from winotify import Notification

USERNAME = ''#学号
PASSWORD = ''#密码
OPERATOR = ''#供应商

# 兼容PyInstaller打包和源码运行
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.abspath(relative_path)

def get_user_ip_mac(session):
    try:
        response = session.get("http://10.2.5.251/", timeout=2)
        ip = re.search(r'user_ip\\s*=\\s*[\'\"](.+?)[\'\"]', response.text)
        mac = re.search(r'user_mac\\s*=\\s*[\'\"](.+?)[\'\"]', response.text)
        return (ip.group(1) if ip else ''), (mac.group(1) if mac else '')
    except Exception as e:
        show_message_box("错误", f"获取IP/MAC失败: {str(e)}")
        return '', ''

def verify_login(session):
    try:
        response = session.get("http://10.2.5.251/", timeout=2)
        return any(x in response.text for x in ("已登录", "注销", "在线数量超过限制"))
    except Exception:
        return False

def show_message_box(title, message):
    Notification(app_id="CUMT自动登录", title=title, msg=message, icon=resource_path("02.png")).show()

def login(session):
    username = USERNAME + ("@xyw" if OPERATOR == "校园网" else "@telecom" if OPERATOR == "中国电信" else "@cmcc" if OPERATOR == "中国移动" else "@unicom")
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
        "Host": "10.2.5.251:801",
        "Referer": "http://10.2.5.251/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
    }
    try:
        timestamp = int(time.time() * 1000)
        callback = f"dr{timestamp}"
        login_url = f"http://10.2.5.251:801/eportal/?c=Portal&a=login&callback={callback}&login_method=1&user_account={username}&user_password={PASSWORD}&wlan_user_ip=&wlan_user_mac=000000000000&wlan_ac_ip=&wlan_ac_name=&jsVersion=3.0&_={timestamp}"
        resp = session.get(login_url, headers=headers, timeout=3)
        json_str = resp.text[resp.text.index('(') + 1 : resp.text.rindex(')')]
        data = json.loads(json_str)
        if data.get('result') == '1' and verify_login(session):
            show_message_box("提示", "登录成功")
            return True
        elif data.get('ret_code') == '1':
            show_message_box("错误", "账号或密码错误")
        elif data.get('ret_code') == '2' or "在线数量超过限制" in data.get('msg', ''):
            show_message_box("提示", "您已经登录过了")
            return True
    except Exception as e:
        show_message_box("错误", f"登录失败: {str(e)}")
    return False

def logout(session):
    if not verify_login(session):
        show_message_box("提示", "您当前未登录")
        return
    try:
        ip, mac = get_user_ip_mac(session)
        timestamp = int(time.time() * 1000)
        callback = f"dr{timestamp}"
        logout_url = f"http://10.2.5.251:801/eportal/?c=Portal&a=logout&callback={callback}&login_method=1&user_account=drcom&user_password=123&ac_logout=0&wlan_user_ip={ip}&wlan_user_ipv6=&wlan_vlan_id=1&wlan_user_mac={mac}&wlan_ac_ip=&wlan_ac_name=&jsVersion=3.0&_={timestamp-22}"
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "Connection": "keep-alive",
            "Host": "10.2.5.251:801",
            "Referer": "http://10.2.5.251/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
        }
        resp = session.get(logout_url, headers=headers, timeout=3)
        json_str = resp.text[resp.text.index('(') + 1 : resp.text.rindex(')')]
        result = json.loads(json_str)
        if result.get('result') == '1':
            show_message_box("提示", "已成功注销")
        else:
            show_message_box("错误", f"注销失败: {result.get('msg', '未知错误')}")
    except Exception as e:
        show_message_box("错误", f"注销时发生错误: {str(e)}")

def main():
    session = requests.Session()
    # login(session)
    logout(session)

if __name__ == '__main__':
    main()
    # time.sleep(1)  # 等待弹窗显示
