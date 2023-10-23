import launch
from launch_ros.actions import Node

def generate_launch_description():
    return launch.LaunchDescription([
        Node(
            package='race_line_optimizer',
            executable='race_line_optimizer',
            name='race_line_optimizer',
            output='screen',
            parameters=[]
        ),
    ])