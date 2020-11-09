#! /bin/python3
#
#  This code derived from the ROS 2 tutorials available at
#  https://index.ros.org/doc/ros2/Tutorials/Writing-A-Simple-Py-Publisher-And-Subscriber/
#
import os
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import sys

class MinimalSubscriber(Node):

    def __init__(self, msg=""):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            String,
            'microk8s_chatter',
            self.listener_callback,
            10)
        self.msg = msg

    def listener_callback(self, msg):
        self.get_logger().info('%s: "%s"' % (self.msg, msg.data))


def main(msg = ""):
    rclpy.init(args=None)
    minimal_subscriber = MinimalSubscriber(msg)

    rclpy.spin(minimal_subscriber)

    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    # Received messages are printed with the format
    #   [TAG:]HOSTNAME:ID: MSG
    # where
    #   TAG      - passed in on startup
    #   HOSTNAME - host name environment variable
    #   ID       - random number assigned to this process
    #   MSG      - message received on the microk8s topic
    msg = ""
    if len (sys.argv) == 2:
        msg += sys.argv[1] + ":"
    msg += os.environ['HOSTNAME']
    msg += ":" + str(os.getpid())
    main(msg)
