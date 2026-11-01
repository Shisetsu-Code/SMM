import bpy, math
from pathlib import Path
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
bpy.ops.mesh.primitive_torus_add(major_radius=1.2, minor_radius=.28)
bpy.context.object.name = "SMM Demo Ring"
material = bpy.data.materials.new("Gold")
material.diffuse_color = (.8, .45, .07, 1)
material.use_nodes = True
bsdf = material.node_tree.nodes.get("Principled BSDF")
bsdf.inputs["Base Color"].default_value = (.8, .45, .07, 1)
bsdf.inputs["Metallic"].default_value = .8
bpy.context.object.data.materials.append(material)
bpy.ops.object.camera_add(location=(3,-5,3))
cam = bpy.context.object
direction = -cam.location
cam.rotation_euler = direction.to_track_quat("-Z","Y").to_euler()
bpy.context.scene.camera = cam
bpy.ops.object.light_add(type="AREA", location=(1,-3,5))
bpy.context.object.data.energy = 900
bpy.context.object.data.shape = "DISK"
bpy.context.object.data.size = 5
bpy.context.scene.world.color = (.12,.12,.12)
Path("scenes").mkdir(exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=str(Path("scenes/demo.blend").resolve()))
