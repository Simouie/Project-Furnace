import bpy


def separate_by_material(obj):

    # abort if object is not mesh

    if obj.type != "MESH": return

    # switch to Object Mode if not already in that mode

    if bpy.context.mode != "OBJECT":
        bpy.ops.object.mode_set(mode="OBJECT")

    # reset selection before going to the next step

    objects = bpy.context.view_layer.objects

    bpy.ops.object.select_all(action="DESELECT")
    objects.active = None

    # select specified object as active object

    obj.select_set(True)
    objects.active = obj

    # switch to Edit Mode to edit mesh

    bpy.ops.object.mode_set(mode="EDIT")

    # separate mesh by material as objects
    # each object should have one material

    bpy.ops.mesh.separate(type="MATERIAL")

    # return to Object Mode before moving on

    bpy.ops.object.mode_set(mode="OBJECT")

    # reset selection before leaving the current context

    bpy.ops.object.select_all(action="DESELECT")
    objects.active = None


def set_default_values(obj):

    flags= [ "portal_ai_deafening_ui", "portal_blocks_sounds_ui", "portal_is_door_ui" ]

    obj.object_type_ui = "_connected_geometry_object_type_mesh"
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
    
    if not obj.get("nwo"): return

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
