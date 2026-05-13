---
name: ros2
description: ROS2 development guidelines. Use when working with ROS2 nodes, packages, launch files, rclpy/rclcpp code, CMakeLists.txt with ament, package.xml, colcon builds, topics/services/actions, QoS settings, lifecycle nodes, TF2 transforms, or any robotics middleware code.
---

# ROS2 Development

Opinionated guidelines for writing robust, production-quality ROS2 code in Python (rclpy) and C++ (rclcpp).

## Node Design

One node, one responsibility. Resist the urge to build multi-purpose nodes — they become untestable.

- Declare **all parameters at construction** with `declare_parameter()`. Reading an undeclared parameter throws at runtime.
- For C++: write **component nodes** (`rclcpp_components`) so they can be loaded into a container process — eliminates per-node process overhead and simplifies lifecycle coordination.
- Use **lifecycle nodes** (`rclcpp_lifecycle::LifecycleNode`) when startup/shutdown sequencing matters — hardware drivers, sensors, stateful processors. Implement all four transitions: `on_configure`, `on_activate`, `on_deactivate`, `on_cleanup`.
- Keep constructors fast. Move blocking initialization (device open, calibration) into `on_configure`.

## Topics vs Services vs Actions

Pick by the communication pattern, not convenience:

| Pattern | Use when |
|---|---|
| Topic (pub/sub) | Continuous streams — sensor data, state, transforms. Fire-and-forget. |
| Service (req/reply) | One-shot synchronous operations that complete fast (<100 ms). |
| Action | Long-running tasks needing feedback and cancellation — navigation, manipulation, planning. |

**Deadlock rule:** Never call a service client inside a callback on the same single-threaded executor. Use async calls or a dedicated callback group on a second thread.

## QoS Profiles

Match QoS to data semantics. Publisher and subscriber QoS must be compatible — a mismatch silently drops the connection. Verify with `ros2 topic info -v`.

```python
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy, HistoryPolicy

# Sensor data — tolerate drops, minimize latency
SENSOR_QOS = QoSProfile(
    reliability=ReliabilityPolicy.BEST_EFFORT,
    durability=DurabilityPolicy.VOLATILE,
    history=HistoryPolicy.KEEP_LAST,
    depth=1,
)

# Control commands — must arrive, keep recent buffer
CONTROL_QOS = QoSProfile(
    reliability=ReliabilityPolicy.RELIABLE,
    durability=DurabilityPolicy.VOLATILE,
    history=HistoryPolicy.KEEP_LAST,
    depth=10,
)

# Latched/transient data (e.g. map, robot description)
LATCHED_QOS = QoSProfile(
    reliability=ReliabilityPolicy.RELIABLE,
    durability=DurabilityPolicy.TRANSIENT_LOCAL,
    history=HistoryPolicy.KEEP_LAST,
    depth=1,
)
```

## Executor Patterns

- **SingleThreadedExecutor**: Default. Safe when no callback blocks.
- **MultiThreadedExecutor + ReentrantCallbackGroup**: Parallel callbacks. All shared state must be thread-safe.
- **MultiThreadedExecutor + MutuallyExclusiveCallbackGroup**: Serialize a subset while parallelizing others — common pattern for mixing a fast sensor callback with a slow processing callback.

Never `time.sleep()` or `rclcpp::sleep_for()` inside a callback. Use a timer node for periodic work.

```python
self.timer = self.create_timer(0.1, self.timer_callback)  # 10 Hz
```

## Parameters

```python
# Declare with type and default at construction
self.declare_parameter('max_speed', 1.0)
self.declare_parameter('frame_id', 'base_link')
self.declare_parameter('topic_name', 'cmd_vel')

# Read typed value
speed = self.get_parameter('max_speed').get_parameter_value().double_value

# Dynamic reconfigure — validate in the callback, return failure on bad input
self.add_on_set_parameters_callback(self._on_params_changed)
```

Load parameters from YAML files in launch — never hardcode values that operators might tune.

## Launch Files (Python)

Prefer Python launch over XML for any non-trivial configuration.

```python
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, GroupAction
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node, PushRosNamespace
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    pkg_share = FindPackageShare('my_package')

    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='false'),
        DeclareLaunchArgument('namespace', default_value='robot'),

        GroupAction([
            PushRosNamespace(LaunchConfiguration('namespace')),
            Node(
                package='my_package',
                executable='my_node',
                name='my_node',
                parameters=[
                    PathJoinSubstitution([pkg_share, 'config', 'params.yaml']),
                    {'use_sim_time': LaunchConfiguration('use_sim_time')},
                ],
                remappings=[('cmd_vel', 'base/cmd_vel')],
                output='screen',
            ),
        ]),
    ])
```

## Package Organization

```
my_package/
├── CMakeLists.txt          # ament_cmake or ament_cmake_python
├── package.xml             # all deps declared here
├── config/
│   └── params.yaml
├── launch/
│   └── my_node.launch.py
├── include/my_package/    # C++ public headers only
├── src/                   # C++ sources
├── my_package/            # Python module (same name as package)
│   ├── __init__.py
│   └── my_node.py
└── test/
    ├── test_my_node.py
    └── test_launch.py
```

## Build & Test

```bash
# Build a package and all its dependencies
colcon build --packages-up-to my_package --symlink-install

# Test one package, see failures immediately
colcon test --packages-select my_package
colcon test-result --all --verbose

# After any build — always source
source install/setup.bash
```

`--symlink-install` avoids rebuilding Python packages on source edits. Don't use it for C++ release builds.

## TF2

- Publish dynamic transforms with `TransformBroadcaster`, static ones with `StaticTransformBroadcaster`.
- Always stamp with current clock: `self.get_clock().now().to_msg()`.
- Buffer lookups: wrap in try/except for `tf2_ros.LookupException`, `tf2_ros.ExtrapolationException`, `tf2_ros.ConnectivityException`.
- Frame naming follows REP-105: `map → odom → base_link → sensor_frame`.

```python
try:
    t = self.tf_buffer.lookup_transform('base_link', 'sensor_frame', rclpy.time.Time())
except (tf2_ros.LookupException, tf2_ros.ExtrapolationException) as e:
    self.get_logger().warn(f'TF lookup failed: {e}')
    return
```

## Error Handling

- Validate inputs at callback entry. Log and return early on invalid data — never silently continue.
- Use severity correctly: `DEBUG` for traces, `INFO` for state transitions, `WARN` for recoverable issues, `ERROR` for failures requiring operator attention.
- Exceptions inside callbacks are swallowed by the executor by default. Log them explicitly.
- Hardware failures: deactivate the lifecycle node, attempt bounded recovery, publish a diagnostic status.

```python
def topic_callback(self, msg):
    if msg.data < 0:
        self.get_logger().warn(f'Negative value received: {msg.data}')
        return
    try:
        self._process(msg)
    except Exception as e:
        self.get_logger().error(f'Processing failed: {e}')
```

## C++ Patterns

```cpp
// Use SharedPtr aliases — never raw node pointers
rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr pub_;
rclcpp::Subscription<sensor_msgs::msg::LaserScan>::SharedPtr sub_;

// Correct callback binding
sub_ = this->create_subscription<sensor_msgs::msg::LaserScan>(
    "scan", rclcpp::SensorDataQoS(),
    std::bind(&MyNode::scan_callback, this, std::placeholders::_1));

// Prefer timer-based polling over spin_some in main
auto node = std::make_shared<MyNode>();
rclcpp::spin(node);  // blocks; use spin_some only if you own the loop
```

## Naming Conventions

- Topics: `snake_case`, verb-object form — `scan`, `cmd_vel`, `joint_states`
- Nodes: `snake_case` — `laser_scan_matcher`, `robot_state_publisher`
- Packages: `snake_case` — `my_robot_bringup`, `sensor_driver`
- Messages/Services: `PascalCase` — `LidarScan.msg`, `SetVelocity.srv`
- Parameters: `snake_case` with dot-separated namespaces — `controller.max_velocity`
