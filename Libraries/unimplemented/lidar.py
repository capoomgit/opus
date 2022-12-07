import omni
import asyncio
from omni.isaac.range_sensor import _range_sensor
from pxr import UsdGeom

stage = omni.usd.get_context().get_stage()               
timeline = omni.timeline.get_timeline_interface() 
lidarInterface = _range_sensor.acquire_lidar_sensor_interface()

# Lidar name
lidarPath = "/Lidar"

# Create lidar prim
result, prim = omni.kit.commands.execute(
            "RangeSensorCreateLidar",
            path=lidarPath,
            parent="/World",
            min_range=0.4,
            max_range=100.0,
            draw_points=True,
            draw_lines=False,
            horizontal_fov=360.0,
            vertical_fov=60.0,
            horizontal_resolution=0.4,
            vertical_resolution=0.4,
            rotation_rate=0.0,
            high_lod=True,
            yaw_offset=0.0,
            enable_semantics=True
        )

# Lidar pos
UsdGeom.XformCommonAPI(prim).SetTranslate((2.0, 0.0, 0.0))

async def get_lidar_param():
    await asyncio.sleep(1.0)
    timeline.pause()
    pointcloud = lidarInterface.get_point_cloud_data("/World"+lidarPath)
    semantics = lidarInterface.get_semantic_data("/World"+lidarPath)

    print("Point Cloud", pointcloud)
    print("Semantic ID", semantics)


timeline.play()
asyncio.ensure_future(get_lidar_param())