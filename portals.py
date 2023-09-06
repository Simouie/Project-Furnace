import bpy


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
    # do not proceed if those are not there for some reason
    
    if not obj.get("nwo"): return

    # directly set values for properties that need to be set for portals
    # without actually interacting with Foundry UI in the same way users do 

    set_default_values(obj.nwo)

    # transfer flags used for Halo materials to object properties
    # each portal should be using one material but there might be empty slots or unused slots
    # the final result might be incorrect if there actually are multiple materials being used
    # that is not normal for Halo so fixing that shall be the responsibility of the user
    
    for slot in obj.material_slots:
        if slot.material.name.startswith("+portal"):
            if not slot.material.get("ass_jms"): continue
            transfer_material_flags(slot.material.ass_jms, obj.nwo)
