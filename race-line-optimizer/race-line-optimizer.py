import rclpy
from rclpy.node import Node
from rclpy.clock import ROSClock
from std_msgs.msg import String
from nav_msgs.msg import Odometry
from std_msgs.msg import Header
from geometry_msgs.msg import PolygonStamped, Point32


class RaceLineOptimizer(Node):

    def __init__(self):
        super().__init__('race_line_optimizer')
        self.publisher_ = self.create_publisher(PolygonStamped, 'optimized_trail', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
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
        
        
def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()