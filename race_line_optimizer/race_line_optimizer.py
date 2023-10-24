#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.clock import ROSClock
from std_msgs.msg import String
from nav_msgs.msg import Odometry
from std_msgs.msg import Header
from geometry_msgs.msg import PolygonStamped, Point32
from scipy.interpolate import CubicSpline
import numpy as np


class RaceLineOptimizer(Node):

    def __init__(self):
        super().__init__('race_line_optimizer')
        self.publisher_ = self.create_publisher(PolygonStamped, 'optimized_trail', 10)
        timer_period = 0.5  # seconds
        #self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0
        self.subscription = self.create_subscription(
            PolygonStamped,
            'slime_trail',
            self.listener_callback,
            10)
        self.subscription 
    #def timer_callback(self):
    #    msg = String()
    #    msg.data = 'Hello World: %d' % self.i
    #    self.publisher_.publish(msg)
    #    self.get_logger().info('Publishing: "%s"' % msg.data)
    #    self.i += 1

    def listener_callback(self, msg: PolygonStamped):
        # Extracting x and y coordinates from the incoming message
        x = [point.x for point in msg.polygon.points]
        y = [point.y for point in msg.polygon.points]

        # Interpolating using cubic spline
        cs = CubicSpline(x, y)

        # Generating new x and y values (You can customize the number of points if needed)
        x_new = np.linspace(min(x), max(x), len(x))
        y_new = cs(x_new)

        # Creating a new PolygonStamped message
        optimized_msg = PolygonStamped()
        optimized_msg.header = Header(stamp=ROSClock().now().to_msg(), frame_id="map")
        optimized_msg.polygon.points = [Point32(x_val, y_val, 0.0) for x_val, y_val in zip(x_new, y_new)]

        # Publishing the optimized message
        self.publisher_.publish(optimized_msg)

        
def main(args=None):
    rclpy.init(args=args)

    race_line_optimizer = RaceLineOptimizer()

    rclpy.spin(race_line_optimizer)
# Destroy the node explicitly
# (optional - otherwise it will be done automatically
# when the garbage collector destroys the node object)
    race_line_optimizer.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()