# Software License Agreement (BSD)
#
# @author    Tony Baltovski <tbaltovski@clearpathrobotics.com>
# @author    Roni Kreinin <rkreinin@clearpathrobotics.com>
# @copyright (c) 2023, Clearpath Robotics, Inc., All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# * Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# * Neither the name of Clearpath Robotics nor the names of its contributors
#   may be used to endorse or promote products derived from this software
#   without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    GroupAction,
    IncludeLaunchDescription,
)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import (
    EnvironmentVariable,
    LaunchConfiguration,
    PathJoinSubstitution,
    FindExecutable 
)
from launch_ros.actions import PushRosNamespace
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():

    # Packages
    pkg_clearpath_control = FindPackageShare('clearpath_control')
    pkg_clearpath_platform_description = FindPackageShare('clearpath_platform_description')
    pkg_roas_description = FindPackageShare('roas2_bringup')

    # Launch Arguments
    arg_setup_path = DeclareLaunchArgument(
        'setup_path',
        default_value='/etc/clearpath/'
    )

    arg_use_sim_time = DeclareLaunchArgument(
        'use_sim_time',
        choices=['true', 'false'],
        default_value='false',
        description='Use simulation time'
    )

    arg_namespace = DeclareLaunchArgument(
        'namespace',
        default_value='',
        description='Robot namespace'
    )

    arg_enable_ekf = DeclareLaunchArgument(
        'enable_ekf',
        default_value='true',
        choices=['true', 'false'],
        description='Enable localization via EKF node'
    )

    # Launch Configurations
    setup_path = LaunchConfiguration('setup_path')
    use_sim_time = LaunchConfiguration('use_sim_time')
    namespace = LaunchConfiguration('namespace')
    enable_ekf = LaunchConfiguration('enable_ekf')

    # Launch files
    launch_file_platform_description = PathJoinSubstitution([
      pkg_roas_description,
      'launch',
      'description.launch.py'])

    launch_file_control = PathJoinSubstitution([
      pkg_clearpath_control,
      'launch',
      'control.launch.py'])

    launch_file_localization = PathJoinSubstitution([
      pkg_clearpath_control,
      'launch',
      'localization.launch.py'])

    launch_file_teleop_base = PathJoinSubstitution([
      pkg_clearpath_control,
      'launch',
      'teleop_base.launch.py'])

    launch_file_teleop_joy = PathJoinSubstitution([
      pkg_clearpath_control,
      'launch',
      'teleop_joy.launch.py'])

    group_platform_action = GroupAction(
        actions=[
            PushRosNamespace(namespace),

            IncludeLaunchDescription(
              PythonLaunchDescriptionSource(launch_file_platform_description),
              launch_arguments=[
                ('setup_path', setup_path),
                ('use_sim_time', use_sim_time),
                ('namespace', namespace),
              ]
            ),

            # Launch clearpath_control/control.launch.py which is just robot_localization.
            IncludeLaunchDescription(
              PythonLaunchDescriptionSource(launch_file_control),
              launch_arguments=[
                ('setup_path', setup_path),
                ('use_sim_time', use_sim_time),
              ]
            ),

            # Launch localization (ekf node)
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(launch_file_localization),
                launch_arguments=[
                  ('setup_path', setup_path),
                  ('use_sim_time', use_sim_time),
                  ('enable_ekf', enable_ekf)
                ]
            ),

            # Launch clearpath_control/teleop_base.launch.py which is various ways to tele-op
            # the robot but does not include the joystick. Also, has a twist mux.
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(launch_file_teleop_base),
                launch_arguments=[
                  ('setup_path', setup_path),
                  ('use_sim_time', use_sim_time),
                ]
            ),

            # Launch clearpath_control/teleop_joy.launch.py which is tele-operation using a
            # physical joystick.
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(launch_file_teleop_joy),
                launch_arguments=[
                  ('setup_path', setup_path),
                  ('use_sim_time', use_sim_time),
                ]
            ),
        ]
    )

    ld = LaunchDescription()
    ld.add_action(arg_setup_path)
    ld.add_action(arg_use_sim_time)
    ld.add_action(arg_namespace)
    ld.add_action(arg_enable_ekf)
    ld.add_action(group_platform_action)
    return ld
