#! /bin/python3
#
#  This code derived from the ROS 2 tutorials available at
#  https://index.ros.org/doc/ros2/Tutorials/Writing-A-Simple-Py-Service-And-Client/
#
import rclpy
from rclpy.node import Node
import socket
from std_msgs.msg import String
from std_srvs.srv import Trigger

#
# This service starts with a trigger message which simply runs the callback.
#
class MinimalService(Node):

  def __init__(self, svcname="worker"):
    super().__init__('worker_service')
    self.srv = self.create_service(Trigger, "worker/" + svcname, self.work_callback)

  def work_callback(self, request, response):
    response.message = 'Work request called'
    response.success = True
    self.get_logger().info(response.message)
    return response

def main(svcname):
  rclpy.init(args=None)
  minimal_service = MinimalService(svcname)

  rclpy.spin(minimal_service)

  minimal_service.destroy_node()
  rclpy.shutdown()

if __name__ == '__main__':
    svcname = "svc_"
    # ensure this service gets a unique name
    svcname += socket.gethostbyname(socket.gethostname()).replace(".","_")
    main(svcname)
