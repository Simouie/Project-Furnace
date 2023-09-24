import bpy


def separate_by_selection():

    # do not try to use this outside of Edit Mode
    # some of the geometry should be already selected

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

    # do not continue if the object is not a mesh

    if obj.type != "MESH": return

    # switch to Object Mode if not already in that mode

    if bpy.context.mode != "OBJECT":
        bpy.ops.object.mode_set(mode="OBJECT")

    objects = bpy.context.view_layer.objects

    # reset selection before going to the next step

    bpy.ops.object.select_all(action="DESELECT")
    objects.active = None

    # select specified object as active object

    obj.select_set(True)
    objects.active = obj

    # switch to Edit Mode to edit mesh

    bpy.ops.object.mode_set(mode="EDIT")

    # separate geometry for portals from everything else

    for index, slot in enumerate(obj.material_slots):

        # do not continue if there is no material in the material slot
        # do not continue if the material is not a material for Halo

        if not slot.material: continue
        if not slot.material.get("ass_jms"): continue

        # exclude geometry for portals

        if "+portal" in slot.material.name: continue

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

    # return to Object Mode before moving on

    bpy.ops.object.mode_set(mode="OBJECT")

    # reset selection before leaving the current context

    bpy.ops.object.select_all(action="DESELECT")
    objects.active = None


def set_default_values(obj):

    flags= [ "portal_ai_deafening_ui", "portal_blocks_sounds_ui", "portal_is_door_ui" ]

    obj.mesh_type_ui = "_connected_geometry_mesh_type_plane"
    obj.plane_type_ui = "_connected_geometry_plane_type_portal"
    obj.portal_type_ui = "_connected_geometry_portal_type_two_way"
    
    for f in flags: setattr(obj, f, False)


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

    # check if the object has properties set up and used by Foundry
    # do not proceed if they are not there for whatever reason
    
    if not obj.get("nwo") and not obj.nwo: return

    # do not continue if there are no materials 
    # there is nothing to do if there are no materials

    # if there are multiple materials
    # assume they are for creating different types of portals
    # separate the geometry by material into multiple objects

    n = len(obj.material_slots)

    if n < 1: return
    if n > 1: separate_by_material(obj)

    # do not continue if the material is not intended for portals
    # do not continue if the material lacks the needed attributes

    material = obj.material_slots[0].material

    if not material.name.startswith("+portal"): return
    if not material.get("ass_jms"): return

    # directly set values for object properties that are needed for portals
    # without actually interacting with Foundry UI in the same way that users do

    set_default_values(obj.nwo)

    # transfer flags used for materials in Halo to object properties
    # most flags do not apply to portals but some of them are for portals

    transfer_material_flags(material.ass_jms, obj.nwo)
