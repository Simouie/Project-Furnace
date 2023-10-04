import bpy


def separate_by_selection():

    # do not try to use this outside Edit Mode
    # geometry that uses the given material should be selected

    if bpy.context.mode != "EDIT_MESH": return

    # try to separate selected geometry

    try: 

        # separate already selected geometry and put that in a new object
        # the operator raises an exception if nothing was actually selected

        bpy.ops.mesh.separate(type="SELECTED")

    except: 

        # someone out there who worked on this thing for Blender actually thought
        # raising an exception is both necessary and better than failing gracefully

        print("bruh")


def separate_by_material(obj):

    # do not try to use this outside Edit Mode

    if bpy.context.mode != "EDIT_MESH": return

    # separate geometry for portals from everything else

    for index, slot in enumerate(obj.material_slots):

        # go to the next slot if there is no material in the material slot
        # go to the next slot if the material is not a material for Halo

        if not slot.material: continue
        if not slot.material.get("ass_jms"): continue

        # exclude geometry for portals

        if not slot.material.name.startswith("+portal"): continue

        # directly setting the active material seems to be incorrect
        # selecting material in user interface changes the active material index
        # setting the index seems to be the correct way to set the active material

        obj.active_material_index = index
        bpy.ops.object.material_slot_select()
    
    separate_by_selection()

    # reset selection before moving on

    bpy.ops.mesh.select_all(action="DESELECT")

    # separate everything else by material

    bpy.ops.mesh.separate(type="MATERIAL")


def transfer_material_flags(material, obj):

    dictionary = {
        "portal_ai_deafening_ui": "ai_deafening",
        "portal_blocks_sounds_ui": "blocks_sound",
        "portal_is_door_ui": "portal_door"
    }

    if material.portal_1_way:
        obj.portal_type_ui = "_connected_geometry_portal_type_one_way"

    if material.portal_vis_blocker:
        obj.portal_type_ui = "_connected_geometry_portal_type_no_way"
    
    for p, f in dictionary.items():
        setattr(obj, p, getattr(material, f))


def set_object_properties(obj):

    # do not continue if there are no materials
    # nothing can be done if there are no materials

    # if there are multiple materials
    # assume they are for creating different types of portals
    # separate the geometry by material into multiple objects

    n = len(obj.material_slots)

    if n < 1: return
    if n > 1: separate_by_material(obj)

    # the remaining geometry should be geometry for one type of portal
    # check all material slots because there might be unused materials

    for slot in obj.material_slots:

        # skip to the next slot if there is no material in the material slot

        if not slot.material: continue
        
        # skip to the next slot if
        # the material is not a material for Halo
        # the material is not for portals in Halo
        
        if not slot.material.get("ass_jms"): continue
        if not slot.material.name.startswith("+portal"): continue

        # directly set values for object properties that are needed for portals
        # without interacting with the Foundry UI in the same way that users do

        obj.nwo.mesh_type_ui = "_connected_geometry_mesh_type_plane"
        obj.nwo.plane_type_ui = "_connected_geometry_plane_type_portal"
        obj.nwo.portal_type_ui = "_connected_geometry_portal_type_two_way"

        # transfer flags used for materials in Halo to object properties
        # most flags do not apply to portals but some of them are for portals

        transfer_material_flags(slot.material.ass_jms, obj.nwo)
