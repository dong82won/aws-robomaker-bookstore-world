import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    world_file_name = "bookstore.world"
    package_dir = get_package_share_directory('aws_robomaker_bookstore_world')
    world_default_path = os.path.join(package_dir, 'worlds', world_file_name)
    gazebo_ros = get_package_share_directory('gazebo_ros')

    use_sim_time = LaunchConfiguration('use_sim_time')
    world_path = LaunchConfiguration('world')
    gui = LaunchConfiguration('gui')

    gazebo_server = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(gazebo_ros, 'launch', 'gzserver.launch.py')),
        launch_arguments={'world': world_path, 'use_sim_time': use_sim_time}.items()
    )

    gazebo_client = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(gazebo_ros, 'launch', 'gzclient.launch.py')),
        condition=IfCondition(gui),
        launch_arguments={'use_sim_time': use_sim_time}.items()
    )

    return LaunchDescription([
        DeclareLaunchArgument('world', default_value=[world_default_path, ''], description='SDF world file'),
        DeclareLaunchArgument(name='gui', default_value='true'), # 기본값 true로 변경
        DeclareLaunchArgument(name='use_sim_time', default_value='true'), # 인자 추가 및 기본값 설정
        gazebo_server,
        gazebo_client
    ])