# Robot tracker 2-DOF
## gioi thieu
Dự án này là hệ thống mô phỏng hoạt động trong môi trường ROS 2 (Humble) và Gazebo. 
## tinh nang
* **Mobile Base:** Sử dụng plugin Differential Drive để mô phỏng cơ chế lái Skid-Steer của bánh xích
* **Manipulator:** Cánh tay 2 bậc tự do (Pan-Tilt) được điều khiển vị trí mượt mà thông qua hệ sinh thái `ros2_control` và `joint_trajectory_controller`.
* **Sensors:** Tích hợp và hiển thị đồng bộ trên RViz:
  * Lidar 360 độ (2 cụm truoc/sau).
  * Camera RGB gắn tại khau 1.
  * Odometry phản hồi từ bộ mã hóa (Encoder) bánh xe.
#sau khi tải về đổi tên package thành assem3

```bash
sudo apt update
# Cài đặt Gazebo
sudo apt install gazebo11 libgazebo11-dev -y

# Cài đặt ROS-Gazebo và các Plugins cảm biến
sudo apt install ros-humble-gazebo-ros-pkgs ros-humble-gazebo-plugins -y

# Cài đặt hệ thần kinh ros2_control cho tay máy
sudo apt install ros-humble-ros2-control ros-humble-ros2-controllers ros-humble-gazebo-ros2-control -y

# Cài đặt gói điều khiển bàn phím
sudo apt install ros-humble-teleop-twist-keyboard -y
```

## run

### Dọn dẹp và Build Workspace
```bash
cd ~/ros2_ws
# Xóa thư mục build cũ (Dọn ổ)
rm -rf build/ install/ log/

# Tự động quét và cài đặt các thư viện ROS 2 còn thiếu
sudo apt update
rosdep update
rosdep install --from-paths src --ignore-src -r -y

# Cấp quyền thực thi cho các file Code điều khiển tay máy
chmod +x src/assem3/scripts/*.py

# Build gói assem3 và nạp môi trường
colcon build --packages-select assem3
source install/setup.bash
```

### Khởi động Môi trường (Terminal 1)

```bash
# Chỉ đường cho Gazebo tìm file .STL
export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:~/ros2_ws/src

# Khởi động Gazebo và RViz
ros2 launch assem3 gazebo.launch.py
```

### Di chuyển Robot (Terminal 2)
Sử dụng gói Teleop mặc định của ROS 2 để phát lệnh `cmd_vel`:

```bash
source /opt/ros/humble/setup.bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```
* `i` / `,` : Tiến / Lùi
* Phím `j` / `l`: Xoay trái / Xoay phải
* Phím `k`: Phanh

### Điều khiển Tay máy
```bash
source ~/ros2_ws/install/setup.bash
ros2 run assem3 arm_teleop_key.py
```
* Phím `w` / `s`: Gập lên / Gập xuống khâu vươn (Pitch)
* Phím `a` / `d`: Xoay trái / Xoay phải đế tay máy (Yaw)
* Phím `r`: Reset tay máy về vị trí Home (0, 0)

## kiem tra mang luoi du lieu cam bien
**Kiểm tra Sơ đồ Node & Topic:**
```bash
rqt_graph
```

**Kiểm tra Tần số quét Cảm biến (Sensors Hz):**
```bash
ros2 topic hz /scan_1          # Lidar 1
ros2 topic hz /camera/image_raw # Camera
```

**Đọc dữ liệu Định vị thời gian thực:**
```bash
ros2 topic echo /odom          # Phản hồi tọa độ bánh xe
ros2 topic echo /joint_states  # Phản hồi góc quay thực tế của tay máy
```

## cau truc

```text
assem3/
├── README.md
├── config/       # controllers.yaml: Cấu hình PID và giao diện cho ros2_control
├── launch/       # gazebo.launch.py: Script khởi động toàn bộ hệ thống & delay node
├── meshes/       # File 3D (.STL) nguyên bản từ phần mềm SolidWorks
├── rviz/         # urdf_config.rviz: Lưu trữ Layout giao diện theo dõi Cảm biến
├── scripts/      # Node Python xử lý Service và nội suy quỹ đạo tay máy
├── urdf/         # assem3.urdf: Lõi vật lý, động học và plugin của robot
├── worlds/       #map tu thiet ke
├── CMakeLists.txt
└── package.xml
```
