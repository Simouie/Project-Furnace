import bpy


def set_default_values(obj):

    flags= [ "portal_ai_deafening_ui", "portal_blocks_sounds_ui", "portal_is_door_ui" ]

    obj.object_type_ui = "_connected_geometry_object_type_mesh"
    obj.mesh_type_ui = "_connected_geometry_mesh_type_plane"
    obj.plane_type_ui = "_connected_geometry_plane_type_portal"
    obj.plane_type_ui = "_connected_geometry_portal_type_two_way"

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
    
    for a, b in dictionary.items():
        setattr(obj, a, getattr(obj, b))


def set_object_properties(obj):

    set_default_values(obj.nwo)

    for slot in obj.material_slots:
        if slot.material.get("ass_jms"):
            transfer_material_flags(slot.material.ass_jms, obj.nwo)
