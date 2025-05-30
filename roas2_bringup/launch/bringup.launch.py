import os
import launch
import launch_ros

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, IncludeLaunchDescription, GroupAction
from launch.substitutions import LaunchConfiguration, Command, PathJoinSubstitution, FindExecutable
from launch_ros.actions import Node, SetRemap, PushRosNamespace

from launch_ros.substitutions import FindPackageShare

from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():


    roas2_bringup_group_action = GroupAction([

        # Jackal Package
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(PathJoinSubstitution(
                [FindPackageShare('roas2_bringup'), 'launch', 'jackal.launch.py']
            )),
        ),

    
        # Ouster Bringup
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(PathJoinSubstitution(
                [FindPackageShare('roas2_bringup'), 'launch', 'include/ouster.launch.py']
            )),
        ),

    ])


    return LaunchDescription([
        roas2_bringup_group_action  
    ])
