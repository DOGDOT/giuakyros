#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts
import sys, select, termios, tty

# Lưu lại cấu hình terminal cũ
settings = termios.tcgetattr(sys.stdin)

msg = """
🎮 ĐIỀU KHIỂN TAY MÁY 2-DOF
---------------------------
Sử dụng các phím sau để quay tay máy:
        w
    a   s   d

w / s : Gập lên / Gập xuống (Pitch)
a / d : Xoay trái / Xoay phải (Yaw)

r : Reset tay máy về góc (0, 0)
CTRL-C để thoát
---------------------------
"""

def getKey():
    # Hàm đọc phím bấm trực tiếp mà không cần ấn Enter
    tty.setraw(sys.stdin.fileno())
    select.select([sys.stdin], [], [], 0)
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

class ArmTeleop(Node):
    def __init__(self):
        super().__init__('arm_teleop')
        self.client = self.create_client(AddTwoInts, '/move_arm')
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Đang tìm kết nối với tay máy...')
        self.pan = 0
        self.tilt = 0
        self.step = 5 # Mỗi lần bấm phím, khớp xoay 5 độ

    def send_request(self):
        req = AddTwoInts.Request()
        req.a = self.pan
        req.b = self.tilt
        self.client.call_async(req)
        # In góc hiện tại ra màn hình
        print(f"\rGóc hiện tại -> Đế (Yaw): {self.pan:^4}° | Khâu (Pitch): {self.tilt:^4}°", end='')

def main(args=None):
    rclpy.init(args=args)
    node = ArmTeleop()
    print(msg)
    
    try:
        while True:
            key = getKey()
            if key == 'w':
                node.tilt += node.step
            elif key == 's':
                node.tilt -= node.step
            elif key == 'a':
                node.pan += node.step
            elif key == 'd':
                node.pan -= node.step
            elif key == 'r':
                node.pan = 0
                node.tilt = 0
            elif key == '\x03': # Phím CTRL+C để thoát
                break
            else:
                continue
            
            # Khóa góc (Không cho gập quá lố gây gãy tay)
            # Theo URDF của bạn: Yaw [-180, 180], Pitch [-90, 90]
            node.pan = max(min(node.pan, 180), -180)
            node.tilt = max(min(node.tilt, 90), -90)
            
            node.send_request()
            
    except Exception as e:
        print(e)
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()