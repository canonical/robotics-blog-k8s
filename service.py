#! /bin/python3
#
#  This code derived from the ROS 2 tutorials available at
#  https://index.ros.org/doc/ros2/Tutorials/Writing-A-Simple-Py-Service-And-Client/
#
import os
import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Trigger
import sys

#
# Start this service by calling it with a trigger message. If the call
# succeeds (returns True), the service does work (i.e., send messages on
# the microk8s topic) for a short time. The call will fail (return False)
# if the service is already busy working.
#
class MinimalService(Node):

  def __init__(self, svc_name = "worker", msg = ""):
    super().__init__('worker_service')
    self.srv = self.create_service(Trigger, svc_name, self.start_work_callback)
    self.msg = msg
    self.total_work = 0
    self.work_completed = 0
    self.working = False

  def start_work_callback(self, request, response):
    if (self.working):
      response.success = False
      response.message = 'Cannot accept new work (currently completed %d of %d)' % (self.work_completed, self.total_work)
      self.get_logger().info('%s: %s' % (self.msg, response.message))
      return response

    response.success = self.start_work()
    response.message = 'Started working, total work is %d' % (self.total_work)
    self.get_logger().info('%s: %s' % (self.msg, response.message))

    return response

  # Queue up work
  def start_work(self):
    self.working = True
    timer_period = 1.0
    self.total_work = int (random() * 20) + 5
    self.work_completed = 0
    self.timer = self.create_timer(timer_period, self.work_callback)
    self.publisher_ = self.create_publisher(String, 'microk8s', 10)
    return self.working

  # Close out work
  def end_work(self):
    self.working = False
    self.total_work = 0
    self.work_completed = 0
    self.destroy_timer (self.timer)
    self.destroy_publisher (self.publisher_)
    return True

  # "Work" is publishing a message on the microk8s topic
  def work_callback(self):
    self.work_completed += 1
    msg = String()
    msg.data = '%s: Completed %d of %d' % (self.msg, self.work_completed, self.total_work)
    self.publisher_.publish(msg)
    self.get_logger().info('Publishing: "%s"' % msg.data)
    if (self.work_completed >= self.total_work):
      self.end_work()


def main(svc_name, msg):
  rclpy.init(args=None)
  minimal_service = MinimalService(svc_name, msg)

  rclpy.spin(minimal_service)

  minimal_publisher.destroy_node()
  rclpy.shutdown()


if __name__ == '__main__':
    # Published message is in the format
    #   SERVICE:HOSTNAME:ID: Completed COUNT of TOTAL
    # where
    #   SERVICE  - ROS service name passed in on startup (defaults to 'worker')
    #   HOSTNAME - host name environment variable
    #   ID       - Random number assigned to this process
    #   COUNT    - number of messages sent in this work cycle
    #   TOTAL    - number of total message to be sent in this work cycle
    if len (sys.argv) == 2:
      svc_name = sys.argv[1]
    else:
      svc_name = "worker"
    if "HOSTNAME" in os.environ.keys():
      hostname = os.environ['HOSTNAME']
    else:
      hostname = ""
    msg = '%s:%s:%s' % (svc_name, hostname, str(os.getpid()))
    main(svc_name, msg)
