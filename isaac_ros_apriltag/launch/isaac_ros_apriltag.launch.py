import launch
from launch.actions import ExecuteProcess
from launch_ros.actions import ComposableNodeContainer
from launch_ros.descriptions import ComposableNode

def generate_launch_description():
    # Define the AprilTag node
    apriltag_node = ComposableNode(
        package='isaac_ros_apriltag',
        plugin='nvidia::isaac_ros::apriltag::AprilTagNode',
        name='apriltag',
        remappings=[('image', 'timon/camera/frontright/image'),
                    ('camera_info', 'timon/camera/frontright/camera_info')],
        parameters=[{'size': 0.038,
                     'max_tags': 64,
                     'tile_size': 4,
                     'backends': 'PVA',
                     'tag_family': 'tag25h9'}]
    )

    # Define the container for AprilTag node
    apriltag_container = ComposableNodeContainer(
        package='rclcpp_components',
        name='apriltag_container',
        namespace='',
        executable='component_container_mt',
        composable_node_descriptions=[
            apriltag_node,
        ],
        output='screen'
    )

    # Launch Zenoh Router using ExecuteProcess
    zenoh_router = ExecuteProcess(
        cmd=['ros2', 'run', 'rmw_zenoh_cpp', 'rmw_zenohd'],
        output='screen'
    )

    return launch.LaunchDescription([
        apriltag_container,
        zenoh_router
    ])
