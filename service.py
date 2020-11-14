#! /bin/python3
#
#  This code derived from the ROS 2 tutorials available at
#  https://index.ros.org/doc/ros2/Tutorials/Writing-A-Simple-Py-Service-And-Client/
#
import os
import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from std_srvs.srv import Trigger

#
# This service starts with a trigger message which simply runs the callback.
#
class MinimalService(Node):

  def __init__(self, hostname="worker"):
    super().__init__('worker_service')
    # The service lives at worker/[hostname] 
    self.srv = self.create_service(Trigger, "worker/" + hostname, self.work_callback)

  def work_callback(self, request, response):
    response.message = 'Service started working'
    response.success = True
    self.get_logger().info(response.message)
    return response

def main(hostname):
  rclpy.init(args=None)
  minimal_service = MinimalService(hostname)

  rclpy.spin(minimal_service)

  minimal_service.destroy_node()
  rclpy.shutdown()


if __name__ == '__main__':
    if "HOSTNAME" in os.environ.keys():
      hostname = os.environ['HOSTNAME']
    else:
      hostname = "localhost"
    main(hostname)
