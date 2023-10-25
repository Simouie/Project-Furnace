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

    if material.transparent_1_sided:
        bpy.ops.nwo.face_layer_add(options="transparent")

    if material.transparent_2_sided:
        bpy.ops.nwo.face_layer_add(options="two_sided")
        bpy.ops.nwo.face_layer_add(options="transparent")

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
    # if material.dislike_photons:
    # if material.ignored_by_lightmaps:
    # if material.blocks_sound:

    if material.decal_offset:
        bpy.ops.nwo.face_layer_add_flags(options="decal_offset")

    # if material.water_surface:

    if material.slip_surface:
        bpy.ops.nwo.face_layer_add_flags(options="slip_surface")

    # if material.group_transparents_by_plane:


def parse_material_name(name, material):

    # check the name of the material for any special symbols
    # enable the corresponding flag for the material

    for c in name: 

        # special symbols should be placed before or after the actual name
        # do not continue if this character is a letter or a number

        if c.isalnum(): return

        # many of these can be used for almost anything within a level
        # some of them are intended only for special types of geometry

        match c:

            case "%": 
                material.two_sided = True
                
            case "#": 
                material.transparent_1_sided = True
                
            case "?": 
                material.transparent_2_sided = True
                
            case "!": 
                material.render_only = True
                
            case "@": 
                material.collision_only = True
                
            case "*": 
                material.sphere_collision_only = True
                
            case "$": 
                material.fog_plane = True
                
            case "^": 
                material.ladder = True
                
            case "-": 
                material.breakable = True
                
            case "&": 
                material.ai_deafening = True
                
            case "=": 
                material.no_shadow = True
                
            case ".": 
                material.shadow_only = True
                
            case ";": 
                material.lightmap_only = True
                
            case ")": 
                material.precise = True
                
            case ">": 
                material.conveyor = True
                
            case "<": 
                material.portal_1_way = True
                
            case "|": 
                material.portal_door = True
                
            case "~": 
                material.portal_vis_blocker = True
                
            case "(": 
                material.dislike_photons = True
                
            case "{": 
                material.ignored_by_lightmaps = True
                
            case "}": 
                material.blocks_sound = True
                
            case "[": 
                material.decal_offset = True
                
            case "'": 
                material.water_surface = True
                
            case "0": 
                material.slip_surface = True
                
            case "]": 
                material.group_transparents_by_plane = True


def add_seam_sealer(mesh):
    
    # do not try to use this outside Edit Mode
    # geometry that uses the given material should be selected

    if bpy.context.mode != "EDIT_MESH": return

    # levels in Halo should not have gaps or holes in its geometry
    # this material is for geometry that seals up those openings

    bpy.ops.nwo.face_layer_add(options="_connected_geometry_face_type_seam_sealer")


def add_sky(material, mesh):

    # do not try to use this outside Edit Mode
    # some geometry should be already selected

    if bpy.context.mode != "EDIT_MESH": return

    # the sky is usually not part of the level
    # geometry that uses this special material will be invisible
    # this allows the sky to be seen through those parts of the level

    bpy.ops.nwo.face_layer_add(options="_connected_geometry_face_type_sky")

    # levels in Halo can reference and use more than one sky
    # materials used to show the sky should have a number at the end of the name
    # that number corresponds to the index of a sky referenced by the level

    index = material.name.split("+sky")[1]
    index = index.split(".")[0]

    if len(index.strip()) <= 0: return

    for c in index:
        if c not in "1234567890": return

    mesh.face_props[-1].sky_permutation_index_ui = int(index)


def set_face_properties(obj):

    # do not try to use this outside Edit Mode

    if bpy.context.mode != "EDIT_MESH": return

    # set up face properties for each material

    for index, slot in enumerate(obj.material_slots):

        # some of the geometry might be selected upon entering Edit Mode
        # reset selection before moving on

        bpy.ops.mesh.select_all(action="DESELECT")
        
        # go to the next slot if
        # the slot has no material
        # the material is not a material for Halo

        if not slot.material: continue
        if not slot.material.get("ass_jms"): continue

        # enable any flags that should be enabled

        names = [ slot.material.name, reversed(slot.material.name) ]

        for name in names:
            parse_material_name(name, slot.material.ass_jms)

        # directly setting the active material seems to be incorrect
        # selecting material in user interface changes the active material index
        # setting the index seems to be the correct way to set the active material

        obj.active_material_index = index
        bpy.ops.object.material_slot_select()

        # some materials are for specific and special uses
        # such materials need to be processed in a different way

        if slot.material.name.startswith("+sky"):
            add_sky(slot.material, obj.data.nwo)
            continue

        if slot.material.name.startswith("+seamsealer"):
            add_seam_sealer(obj.data.nwo)
            continue

        # add and modify face properties according to the material

        transfer_material_flags(slot.material.ass_jms)
        transfer_lightmap_resolution_properties(slot.material.ass_jms, obj.data.nwo)
        transfer_lightmap_properties(slot.material.ass_jms, obj.data.nwo)

        # reset selection before moving on

        bpy.ops.mesh.select_all(action="DESELECT")
