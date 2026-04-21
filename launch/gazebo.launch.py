import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    pkg_share = get_package_share_directory('assem3')
    
    # 1. Trỏ đường dẫn tới file my_world.world
    world_path = os.path.join(pkg_share, 'worlds', 'my_world.world')

    # 2. Khởi động Gazebo và nạp file world này (BIẾN NÀY ĐÚNG)
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
        launch_arguments={'world': world_path}.items() 
    )
    
    urdf_file = os.path.join(pkg_share, 'urdf', 'assem3.urdf')
    rviz_config_file = os.path.join(pkg_share, 'rviz', 'urdf_config.rviz')
    
    # Bắt đường dẫn tuyệt đối của file YAML
    controller_file = os.path.join(pkg_share, 'config', 'controllers.yaml')

    with open(urdf_file, 'r') as infp:
        robot_desc = infp.read()

    # Chèn trực tiếp đường dẫn YAML vào URDF để chống sập nguồn 
    robot_desc = robot_desc.replace('ABSOLUTE_PATH_TO_YAML', controller_file)

    rsp_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_desc, 'use_sim_time': True}]
    )

    spawn_entity_node = Node(
        package='gazebo_ros', 
        executable='spawn_entity.py',
        arguments=['-entity', 'my_tank', '-topic', 'robot_description', '-z', '0.2'], 
        output='screen'
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config_file]
    )

    # --- NHÓM ĐIỀU KHIỂN TAY MÁY ---
    broadcaster_spawner = Node(
        package="controller_manager", executable="spawner", arguments=["joint_state_broadcaster"]
    )
    arm_spawner = Node(
        package="controller_manager", executable="spawner", arguments=["arm_controller"]
    )
    python_arm_node = Node(
        package='assem3', executable='arm_node.py', output='screen'
    )

    # TRÌ HOÃN 3 GIÂY
    delay_spawners = TimerAction(
        period=3.0,
        actions=[broadcaster_spawner, arm_spawner, python_arm_node]
    )

    # 3. GỌI ĐÚNG BIẾN "gazebo" CHỨA THẾ GIỚI CỦA BẠN VÀO ĐÂY
    return LaunchDescription([
        rsp_node,
        gazebo,  # <----- CHÍNH LÀ CHỖ NÀY!
        spawn_entity_node,
        rviz_node,
        delay_spawners
    ])