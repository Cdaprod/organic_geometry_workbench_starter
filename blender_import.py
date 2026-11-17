"""Optional Blender renderer. Run blender --background --python blender_import.py -- path/to/model.stl
Requires Blender 4.x+; fallback for older installations.
"""
import sys
import bpy
from mathutils import Vector
from pathlib import Path

path=Path(sys.argv[sys.argv.index('--')+1]).resolve()
if not path.exists(): raise FileNotFoundError(path)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
try:
    bpy.ops.wm.stl_import(filepath=str(path))
except (AttributeError, RuntimeError):
    bpy.ops.import_mesh.stl(filepath=str(path))
obj=bpy.context.object
obj.name=path.stem
mat=bpy.data.materials.new('Satin titanium')
mat.diffuse_color=(0.25,0.43,0.55,1)
mat.use_nodes=True
bsdf=mat.node_tree.nodes.get('Principled BSDF')
bsdf.inputs['Base Color'].default_value=(0.25,0.43,0.55,1)
bsdf.inputs['Metallic'].default_value=.55
bsdf.inputs['Roughness'].default_value=.36
obj.data.materials.append(mat)
for poly in obj.data.polygons: poly.use_smooth=True
# Give smooth shading without claiming the geometry itself is smooth or structurally adequate.
cam_data=bpy.data.cameras.new('Iso camera');cam=bpy.data.objects.new('Iso camera',cam_data)
bpy.context.scene.collection.objects.link(cam)
center=sum((Vector(c) for c in obj.bound_box),Vector())/8
center=obj.matrix_world@center
size=max(obj.dimensions)
cam.location=center+Vector((size*.8,-size*.75,size*.6))
orientation=(center-cam.location).to_track_quat('-Z','Y')
cam.rotation_euler=orientation.to_euler();cam_data.type='ORTHO';cam_data.ortho_scale=size*1.65
bpy.context.scene.camera=cam
for loc,power in [((size*.45,-size*.4,size*1.3),1100),((-size*.6,-size*.3,size*.8),700)]:
    data=bpy.data.lights.new('Softbox','AREA');data.energy=power;data.shape='DISK';data.size=size*.8
    lamp=bpy.data.objects.new('Softbox',data);bpy.context.scene.collection.objects.link(lamp)
    lamp.location=center+Vector(loc);lamp.rotation_euler=(center-lamp.location).to_track_quat('-Z','Y').to_euler()
scene=bpy.context.scene
scene.render.engine='BLENDER_EEVEE_NEXT' if bpy.app.version >= (4,2,0) else 'BLENDER_EEVEE'
scene.render.resolution_x=1280;scene.render.resolution_y=900;scene.render.resolution_percentage=100
scene.world.color=(.10,.11,.13)
scene.render.image_settings.file_format='PNG'
scene.render.filepath=str(path.with_suffix('.blender.png'))
bpy.ops.wm.save_as_mainfile(filepath=str(path.with_suffix('.blend')))
bpy.ops.render.render(write_still=True)
print('Wrote',scene.render.filepath)
