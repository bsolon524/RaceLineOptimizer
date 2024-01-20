import rclpy
from rclpy.node import Node
from rclpy.clock import ROSClock
from std_msgs.msg import String
from nav_msgs.msg import Odometry
from std_msgs.msg import Header
from geometry_msgs.msg import PolygonStamped, Point32
import numpy as np
from scipy.interpolate import CubicSpline


class RaceLineOptimizer(Node):

    def __init__(self):
        super().__init__('race_line_optimizer')
        self.publisher_ = self.create_publisher(PolygonStamped, 'optimized_trail', 10)
        self.subscription = self.create_subscription(
            PolygonStamped,
            'polygon_topic',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg: PolygonStamped):
        # Extract x and y coordinates from the received message
        x = np.array([point.x for point in msg.polygon.points])
        y = np.array([point.y for point in msg.polygon.points])
    
        # Data smoothing (using a simple moving average for example)
        window_size = 12  # or choose another suitable size
        x_smooth = np.convolve(x, np.ones(window_size)/window_size, mode='valid')
        y_smooth = np.convolve(y, np.ones(window_size)/window_size, mode='valid')
    
        # Ensure start and end points are the same for periodicity
        x_smooth[0] = x_smooth[-1]
        y_smooth[0] = y_smooth[-1]
    
        # Create a pseudo-time parameter
        t = np.arange(len(x_smooth))
    
        # Create parametric splines
        spline_x = CubicSpline(t, x_smooth, bc_type='periodic')
        spline_y = CubicSpline(t, y_smooth, bc_type='periodic')
    
        # Interpolate using the splines with more t-values for a smoother curve
        t_new = np.linspace(0, len(x_smooth)-1, len(x_smooth)*10)  # 10 times more points
        x_new = spline_x(t_new)
        y_new = spline_y(t_new)

        # Create a new PolygonStamped message for the optimized trail
        optimized_trail = PolygonStamped()
        optimized_trail.header = msg.header  # Use the same header from the received message
        optimized_trail.polygon.points = [Point32(x=x_val, y=y_val) for x_val, y_val in zip(x_new, y_new)]
    
        # Publish the optimized trail
        self.publisher_.publish(optimized_trail)


def main(args=None):
    rclpy.init(args=args)

    race_line_optimizer = RaceLineOptimizer()

    rclpy.spin(race_line_optimizer)

    race_line_optimizer.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
