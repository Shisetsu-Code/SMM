import bpy, sys
args = sys.argv[sys.argv.index("--") + 1:]
path, resolution, samples = args[0], int(args[1]), int(args[2])
scene = bpy.context.scene
scene.render.engine = "CYCLES"
scene.cycles.samples = samples
scene.render.resolution_x = resolution
scene.render.resolution_y = resolution
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.render.filepath = path
bpy.ops.render.render(write_still=True)
