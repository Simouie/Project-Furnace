import bpy 


def transfer_lightmap_properties(material, mesh):

    # do not try to use this outside Edit Mode
    # geometry that uses the given material should be selected

    if bpy.context.mode != "EDIT_MESH": return

    # not all materials for Halo need to have lightmap properties
    # do the following only if the power was not set to the default value

    if material.power > 0:

        # set up lightmap properties
        # almost everything is available in the face property

        bpy.ops.nwo.face_layer_add(options="emissive")

        mesh.face_props[-1].material_lighting_emissive_color_ui = material.color
        mesh.face_props[-1].material_lighting_emissive_power_ui = material.power
        mesh.face_props[-1].material_lighting_emissive_quality_ui = material.quality
        mesh.face_props[-1].material_lighting_emissive_focus_ui = material.emissive_focus

        # attenuation seems to be ignored by Foundry 0.9.3
        # maybe these will be usable in the future

        if material.attenuation_enabled:
           mesh.face_props[-1].material_lighting_attenuation_falloff_ui = material.falloff_distance
           mesh.face_props[-1].material_lighting_attenuation_cutoff_ui = material.cutoff_distance

        # in materials set up by the Halo Asset Blender Development Toolset
        # this is grouped with the lightmap resolution properties

        mesh.face_props[-1].material_lighting_use_shader_gel_ui = material.use_shader_gel

        # the terminology is different but these two things seem to be similar
        # assume they are equivalent or at least similar enough in their purpose

        mesh.face_props[-1].material_lighting_emissive_per_unit_ui = material.power_per_unit_area


def transfer_lightmap_resolution_properties(material, mesh):

    # do not try to use this outside Edit Mode
    # geometry that uses the given material should be selected

    if bpy.context.mode != "EDIT_MESH": return

    # the default color of the two-sided transparency tint is black
    # ignore the two-sided transparency tint if the color is not something else

    if material.additive_transparency.hsv[2] > 0.000:
        bpy.ops.nwo.face_layer_add_lightmap(options="lightmap_additive_transparency")
        mesh.face_props[-1].lightmap_additive_transparency_ui = material.additive_transparency

    # the default color for additive transparency is black 
    # set up additive transparency only if the color is something else

    if material.two_sided_transparent_tint.hsv[2] > 0.000:
        bpy.ops.nwo.face_layer_add_lightmap(options="lightmap_translucency_tint_color")
        mesh.face_props[-1].lightmap_translucency_tint_color_ui = material.two_sided_transparent_tint

    # when setting lightmap resolution scale in the Foundry UI
    # the range of possible values is limited to whole numbers in the range [0, 7]

    # the lightmap resolution scale in materials for Halo 3 is different
    # the range of possible values includes 0 and numbers greater than 0

    # the default value Foundry uses for lightmap resolution scale seems to be 3
    # the default value used by the Halo Asset Blender Development Toolset seems to be 1

    if material.lightmap_res < 1.00:
        bpy.ops.nwo.face_layer_add_lightmap(options="lightmap_resolution_scale")
        mesh.face_props[-1].lightmap_resolution_scale_ui = 1

    if material.lightmap_res > 1.00:
        bpy.ops.nwo.face_layer_add_lightmap(options="lightmap_resolution_scale")
        mesh.face_props[-1].lightmap_resolution_scale_ui = 5


def transfer_material_flags(material):

    # do not try to use this outside Edit Mode
    # geometry that uses the given material should be selected

    if bpy.context.mode != "EDIT_MESH": return

    # for the various flags that can be set for the material
    # set up a face property if the flag is enabled

    # some of the flags will be ignored
    # some of them are not available in the Foundry UI
    # some of them are for special types of objects

    if material.two_sided:
        bpy.ops.nwo.face_layer_add(options="two_sided")

    # if material.transparent_1_sided:
    # if material.transparent_2_sided: 

    if material.render_only:
        bpy.ops.nwo.face_layer_add(options="_connected_geometry_face_mode_render_only")

    if material.collision_only:
        bpy.ops.nwo.face_layer_add(options="_connected_geometry_face_mode_collision_only")

    if material.sphere_collision_only:
        bpy.ops.nwo.face_layer_add(options="_connected_geometry_face_mode_sphere_collision_only")

    # if material.fog_plane:

    if material.ladder:
        bpy.ops.nwo.face_layer_add_flags(options="ladder")

    if material.breakable:
        bpy.ops.nwo.face_layer_add(options="_connected_geometry_face_mode_breakable")

    # if material.ai_deafening:

    if material.no_shadow:
        bpy.ops.nwo.face_layer_add_flags(options="no_shadow")

    if material.shadow_only:
        bpy.ops.nwo.face_layer_add(options="_connected_geometry_face_mode_shadow_only")

    if material.lightmap_only:
        bpy.ops.nwo.face_layer_add(options="_connected_geometry_face_mode_lightmap_only")

    if material.precise:
        bpy.ops.nwo.face_layer_add(options="precise_position")

    # if material.conveyor:
    # if material.portal_1_way:
    # if material.portal_door:
    # if material.portal_vis_blocker:
    # if material.ignored_by_lightmaps:
    # if material.blocks_sound:

    if material.decal_offset:
        bpy.ops.nwo.face_layer_add_flags(options="decal_offset")

    # if material.water_surface:

    if material.slip_surface:
        bpy.ops.nwo.face_layer_add_flags(options="slip_surface")

    # if material.group_transparents_by_plane:


def set_face_properties(obj):

    # do not try to use this outside Edit Mode

    if bpy.context.mode != "EDIT_MESH": return

    # set up face properties for each material

    for index, slot in enumerate(obj.material_slots):

        # directly setting the active material seems to be incorrect
        # selecting material in user interface changes the active material index
        # setting the index seems to be the correct way to set the active material

        obj.active_material_index = index
        bpy.ops.object.material_slot_select()

        # go to the next slot if
        # the slot has no material
        # the material is not a material for Halo

        if not slot.material: continue
        if not slot.material.get("ass_jms"): continue

        # set up face properties without interacting with the Foundry UI
        # the process may be rather slow because it does rely on operators

        transfer_material_flags(slot.material.ass_jms)
        transfer_lightmap_resolution_properties(slot.material.ass_jms, obj.data.nwo)
        transfer_lightmap_properties(slot.material.ass_jms, obj.data.nwo)

        # reset selection before moving on

        bpy.ops.mesh.select_all(action="DESELECT")
