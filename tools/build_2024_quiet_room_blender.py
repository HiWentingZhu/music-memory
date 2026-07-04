from math import cos, radians, sin
from pathlib import Path

import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets" / "models" / "source" / "2024-quiet-room.blend"
EXPORT = ROOT / "assets" / "models" / "rooms" / "2024-quiet-room.glb"


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()


def material(name, color, roughness=0.7, metallic=0.0, emission=None, emission_strength=0.0, alpha=1.0):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = color
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Alpha"].default_value = alpha
    if emission:
        bsdf.inputs["Emission Color"].default_value = emission
        bsdf.inputs["Emission Strength"].default_value = emission_strength
    if alpha < 1:
        mat.blend_method = "BLEND"
        mat.use_screen_refraction = True
    return mat


MATS = {}


def init_materials():
    MATS.update(
        cream=material("soft_cream_shell", (0.88, 0.82, 0.72, 1), 0.52),
        plaster=material("warm_plaster_wall", (0.78, 0.75, 0.66, 1), 0.82),
        floor=material("sage_clay_floor", (0.48, 0.6, 0.46, 1), 0.76),
        sage=material("sage_lounge_fabric", (0.55, 0.66, 0.5, 1), 0.88),
        pillow=material("cream_pillow", (0.9, 0.86, 0.76, 1), 0.82),
        blanket=material("soft_blanket", (0.72, 0.76, 0.62, 1), 0.86),
        wood=material("light_walnut", (0.54, 0.38, 0.22, 1), 0.7),
        paper=material("paper_notes", (0.86, 0.82, 0.7, 1), 0.9),
        gold=material("muted_gold_frame", (0.76, 0.55, 0.25, 1), 0.42, 0.12),
        mountain=material("misty_mountain_relief", (0.48, 0.57, 0.47, 1), 0.74),
        glass=material("muted_glass_calendar", (0.62, 0.82, 0.75, 0.45), 0.25, 0.0, alpha=0.45),
        record=material("record_black", (0.015, 0.014, 0.013, 1), 0.38),
        label=material("record_label_warm", (0.78, 0.58, 0.26, 1), 0.55),
        lamp=material("lamp_glow_material", (1.0, 0.82, 0.42, 1), 0.32, emission=(1, 0.7, 0.25, 1), emission_strength=1.8),
        wave=material("wave_line_glow", (1, 0.88, 0.45, 1), 0.28, emission=(1, 0.76, 0.22, 1), emission_strength=2.0),
    )


def bevel_object(obj, amount=0.035, segments=5):
    bevel = obj.modifiers.new("soft_clay_bevel", "BEVEL")
    bevel.width = amount
    bevel.segments = segments
    bevel.affect = "EDGES"
    obj.modifiers.new("soft_shade_weighted_normals", "WEIGHTED_NORMAL")
    return obj


def cube_obj(name, loc, scale, mat, rot=(0, 0, 0), bevel=0.025):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(mat)
    if bevel:
        bevel_object(obj, bevel, 6)
    return obj


def cyl_obj(name, loc, radius, depth, mat, vertices=48, rot=(0, 0, 0), bevel=False):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=loc, rotation=rot)
    obj = bpy.context.object
    obj.name = name
    obj.data.materials.append(mat)
    bpy.ops.object.shade_smooth()
    if bevel:
        bevel_object(obj, 0.015, 4)
    return obj


def uv_sphere(name, loc, scale, mat):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=24, radius=1, location=loc)
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    obj.data.materials.append(mat)
    bpy.ops.object.shade_smooth()
    return obj


def fan_mesh(name, inner, outer, start_deg, end_deg, z_offset, mat, thickness=0.07):
    verts = []
    faces = []
    steps = 48
    start = radians(start_deg)
    end = radians(end_deg)
    for layer, y in enumerate([0, -thickness]):
        for i in range(steps + 1):
            t = start + (end - start) * i / steps
            verts.append((sin(t) * inner, y, cos(t) * inner + z_offset))
            verts.append((sin(t) * outer, y, cos(t) * outer + z_offset))
    for i in range(steps):
        a = i * 2
        faces.append((a, a + 1, a + 3, a + 2))
        b = (steps + 1) * 2 + i * 2
        faces.append((b + 2, b + 3, b + 1, b))
        faces.append((a + 1, b + 1, b + 3, a + 3))
        faces.append((a, a + 2, b + 2, b))
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(mat)
    bevel_object(obj, 0.025, 5)
    return obj


def curved_wall_mesh(name, radius, start_deg, end_deg, z_offset, height, mat, thickness=0.04):
    verts = []
    faces = []
    steps = 72
    start = radians(start_deg)
    end = radians(end_deg)
    for side, r in enumerate([radius, radius + thickness]):
        for i in range(steps + 1):
            t = start + (end - start) * i / steps
            x = sin(t) * r
            z = cos(t) * r + z_offset
            verts.append((x, 0, z))
            verts.append((x, height, z))
    for i in range(steps):
        a = i * 2
        faces.append((a, a + 2, a + 3, a + 1))
        b = (steps + 1) * 2 + i * 2
        faces.append((b + 1, b + 3, b + 2, b))
        faces.append((a, b, b + 2, a + 2))
        faces.append((a + 1, a + 3, b + 3, b + 1))
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(mat)
    bevel_object(obj, 0.012, 4)
    return obj


def arc_tube(name, radius, start_deg, end_deg, z_offset, y, mat, bevel_depth=0.045):
    points = []
    for i in range(64):
        t = radians(start_deg + (end_deg - start_deg) * i / 63)
        points.append((sin(t) * radius, y, cos(t) * radius + z_offset))
    return curve_tube(name, points, mat, bevel_depth)


def curve_tube(name, points, mat, bevel_depth=0.018):
    curve = bpy.data.curves.new(name, "CURVE")
    curve.dimensions = "3D"
    curve.resolution_u = 18
    curve.bevel_depth = bevel_depth
    curve.bevel_resolution = 5
    spline = curve.splines.new("POLY")
    spline.points.add(len(points) - 1)
    for point, co in zip(spline.points, points):
        point.co = (co[0], co[1], co[2], 1)
    obj = bpy.data.objects.new(name, curve)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(mat)
    return obj


def build_room():
    # 2024 concept shape: an upright rounded rectangular showcase, not a fan room.
    cube_obj("rounded_back_display_wall", (0, 1.04, -0.82), (1.9, 1.9, 0.08), MATS["plaster"], (0, 0, 0), 0.075)
    cube_obj("left_thick_cream_side_frame", (-1.04, 1.02, -0.48), (0.18, 2.05, 0.72), MATS["cream"], (0, 0.06, 0), 0.075)
    cube_obj("right_thick_cream_side_frame", (1.04, 1.02, -0.48), (0.18, 2.05, 0.72), MATS["cream"], (0, -0.06, 0), 0.075)
    cube_obj("rounded_top_cream_cap", (0, 2.03, -0.58), (2.12, 0.22, 0.54), MATS["cream"], (0, 0, 0), 0.09)
    cube_obj("rounded_bottom_cream_plinth", (0, 0.02, -0.1), (2.08, 0.18, 1.24), MATS["cream"], (0, 0, 0), 0.09)
    cube_obj("inset_sage_floor", (0, 0.12, -0.06), (1.72, 0.08, 1.06), MATS["floor"], (0, 0, 0), 0.045)
    cube_obj("inner_shadow_reveal_top", (0, 1.84, -0.49), (1.74, 0.06, 0.08), MATS["glass"], (0, 0, 0), 0.012)
    cube_obj("inner_shadow_reveal_left", (-0.86, 0.96, -0.49), (0.05, 1.62, 0.08), MATS["glass"], (0, 0, 0), 0.012)
    cube_obj("inner_shadow_reveal_right", (0.86, 0.96, -0.49), (0.05, 1.62, 0.08), MATS["glass"], (0, 0, 0), 0.012)

    for i in range(4):
        x = -0.54 + i * 0.36
        cube_obj(f"soft_wall_panel_rib_{i+1}", (x, 1.03, -0.765), (0.012, 1.35, 0.028), MATS["cream"], (0, 0, 0), 0.004)

    cyl_obj("sage_lounge_chair_seat", (-0.3, 0.29, 0.02), 0.36, 0.18, MATS["sage"], 72, (radians(90), 0, 0), True)
    cyl_obj("sage_lounge_chair_inner_cushion", (-0.3, 0.34, 0.02), 0.24, 0.08, MATS["sage"], 72, (radians(90), 0, 0), True)
    cube_obj("cream_pillow_on_chair", (-0.18, 0.44, 0.02), (0.3, 0.12, 0.2), MATS["pillow"], (0, 0.08, -0.08), 0.045)
    cube_obj("soft_blanket_on_chair", (0.02, 0.31, 0.12), (0.2, 0.055, 0.44), MATS["blanket"], (0.16, -0.06, 0), 0.035)

    cube_obj("small_side_table", (-0.72, 0.25, -0.16), (0.24, 0.32, 0.22), MATS["wood"], (0, 0, 0), 0.03)
    cyl_obj("lamp_stem", (-0.72, 0.58, -0.16), 0.025, 0.42, MATS["gold"], 24, (0, 0, 0), False)
    cyl_obj("lamp_glow", (-0.72, 0.84, -0.16), 0.13, 0.18, MATS["lamp"], 48, (0, 0, 0), True)
    bpy.ops.object.light_add(type="POINT", location=(-0.82, 0.86, -0.04))
    lamp_light = bpy.context.object
    lamp_light.name = "lamp_point_light"
    lamp_light.data.color = (1, 0.78, 0.42)
    lamp_light.data.energy = 120
    lamp_light.data.shadow_soft_size = 1.1

    for row in range(3):
        for col in range(3):
            cube_obj(f"calendar_tile_{row*3+col+1}", (0.45 + col * 0.15, 0.9 + row * 0.18, -0.72), (0.12, 0.14, 0.025), MATS["glass"], (0, 0, 0), 0.014)

    cube_obj("left_wall_art_frame", (-0.45, 1.37, -0.72), (0.26, 0.43, 0.032), MATS["gold"], (0, 0, 0), 0.015)
    cube_obj("left_wall_art_paper", (-0.45, 1.37, -0.69), (0.2, 0.35, 0.022), MATS["paper"], (0, 0, 0), 0.01)
    cube_obj("center_wall_art_frame", (-0.08, 1.49, -0.72), (0.24, 0.35, 0.032), MATS["gold"], (0, 0, 0), 0.015)
    cube_obj("center_wall_art_paper", (-0.08, 1.49, -0.69), (0.18, 0.28, 0.022), MATS["paper"], (0, 0, 0), 0.01)
    cyl_obj("wall_record_disc_1", (-0.63, 1.07, -0.69), 0.13, 0.025, MATS["record"], 64, (radians(90), 0, 0), False)
    cyl_obj("wall_record_label_1", (-0.63, 1.07, -0.66), 0.048, 0.016, MATS["label"], 64, (radians(90), 0, 0), False)

    curve_tube("mountain_relief_line_1", [(-0.72, 1.08, -0.685), (-0.45, 1.3, -0.685), (-0.2, 1.16, -0.685), (0.05, 1.34, -0.685), (0.28, 1.18, -0.685)], MATS["mountain"], 0.008)
    curve_tube("mountain_relief_line_2", [(-0.76, 0.96, -0.68), (-0.5, 1.12, -0.68), (-0.28, 1.02, -0.68), (-0.02, 1.18, -0.68), (0.28, 1.04, -0.68)], MATS["mountain"], 0.006)
    curve_tube("bamboo_stem_1", [(0.78, 1.05, -0.69), (0.79, 1.25, -0.69), (0.8, 1.48, -0.69)], MATS["mountain"], 0.008)
    curve_tube("bamboo_stem_2", [(0.86, 0.98, -0.69), (0.85, 1.18, -0.69), (0.86, 1.42, -0.69)], MATS["mountain"], 0.006)

    cube_obj("paper_note_1", (0.22, 0.16, 0.38), (0.28, 0.018, 0.18), MATS["paper"], (0, 0.28, 0), 0.01)
    cube_obj("paper_note_2", (0.44, 0.16, 0.28), (0.22, 0.018, 0.15), MATS["paper"], (0, -0.25, 0), 0.01)
    cyl_obj("small_tea_cup", (0.54, 0.23, 0.04), 0.055, 0.09, MATS["pillow"], 32, (0, 0, 0), True)

    curve_tube("wave_line", [(-0.72, 0.67, 0.12), (-0.48, 0.66, 0.02), (-0.2, 0.73, 0.1), (0.04, 0.64, -0.02), (0.32, 0.72, 0.08), (0.72, 0.66, -0.02)], MATS["wave"], 0.02)

    bpy.ops.object.empty_add(type="PLAIN_AXES", location=(0, 0.75, -0.2))
    bpy.context.object.name = "room_focus_target"


def setup_scene():
    bpy.context.scene.render.engine = "CYCLES"
    bpy.context.scene.cycles.samples = 96
    bpy.context.scene.view_settings.view_transform = "Filmic"
    bpy.context.scene.view_settings.look = "Medium High Contrast"
    bpy.ops.object.light_add(type="AREA", location=(-2.4, 4.2, 3.6))
    key = bpy.context.object
    key.name = "large_softbox_key_light"
    key.data.energy = 550
    key.data.size = 5.2
    bpy.ops.object.camera_add(location=(0, 2.25, 5.3), rotation=(radians(67), 0, 0))
    camera = bpy.context.object
    bpy.context.scene.camera = camera
    camera.name = "preview_camera"
    camera.data.lens = 48


def export_files():
    SOURCE.parent.mkdir(parents=True, exist_ok=True)
    EXPORT.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE))
    bpy.ops.export_scene.gltf(
        filepath=str(EXPORT),
        export_format="GLB",
        export_apply=True,
        export_animations=False,
        export_lights=True,
    )


def main():
    clear_scene()
    init_materials()
    build_room()
    setup_scene()
    export_files()


if __name__ == "__main__":
    main()
