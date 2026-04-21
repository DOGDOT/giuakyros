#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
import math

class ArmControlNode(Node):
    def __init__(self):
        super().__init__('arm_control_node')
        # Dùng mẹo lấy service AddTwoInts (a = khớp 1, b = khớp 2)
        self.srv = self.create_service(AddTwoInts, 'move_arm', self.move_arm_callback)
        self.publisher_ = self.create_publisher(JointTrajectory, '/arm_controller/joint_trajectory', 10)
        self.get_logger().info('Dịch vụ /move_arm đã sẵn sàng! Hãy truyền góc (Độ) cho tôi.')

    def move_arm_callback(self, request, response):
        # Đổi từ Độ sang Radian
        angle1 = math.radians(request.a)
        angle2 = math.radians(request.b)

        msg = JointTrajectory()
        msg.joint_names = ['dexoay_joint', 'khau1_joint']

        point = JointTrajectoryPoint()
        point.positions = [float(angle1), float(angle2)]
        point.time_from_start.sec = 2  # Chuyển động diễn ra mượt mà trong 2 giây

        msg.points.append(point)
        self.publisher_.publish(msg)

        self.get_logger().info(f'Đang di chuyển: Đế xoay {request.a}°, Khâu vươn {request.b}°')
        response.sum = 1 # 1 nghĩa là thành công
        return response

def main():
    rclpy.init()
    node = ArmControlNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()