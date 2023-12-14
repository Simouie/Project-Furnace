import bpy


def for_instance_geometry(obj, prefix="%"):

    # check if the object is intended to be instance geometry for Halo
    # the name of the object should start with the symbol % in most situations

    if not obj.name.startswith(prefix): return False

    # check if the object can have meshes
    # there should be geometry for instance geometry
 
    if not obj.type == "MESH": return False
        
    # the object seems to qualify as instance geometry
    # according to the basic tests written above

    return True


def parse_object_name(name, obj):

    # check the name for special symbols
    # change the object properties according to those symbols

    for c in name: 

        # special symbols should be placed before the actual name
        # do not continue if this character is a letter or a number

        if c.isalnum(): return

        # there are a number of symbols that can be used for instance geometry
        # many of the symbols affect interaction with other things in Halo
        # some of them are simply for adjusting lighting and pathfinding
        
        match c:

            case "!":
                obj.poop_lighting_ui = "_connected_geometry_poop_lighting_per_pixel"

            case "?":
                obj.poop_lighting_ui = "_connected_geometry_poop_lighting_per_vertex"

            case "-":
                obj.poop_pathfinding_ui = "_connected_poop_instance_pathfinding_policy_none"

            case "+":
                obj.poop_pathfinding_ui = "_connected_poop_instance_pathfinding_policy_static"
                
            case "*":
                obj.poop_render_only_ui = True

            case "&":
                obj.poop_chops_portals_ui = True

            case "^":
                obj.poop_does_not_block_aoe_ui = True

            case "<":
                obj.poop_excluded_from_lightprobe_ui = True
                
            case "|":
                obj.decal_offset_ui = True


def set_object_properties(obj):

    # directly set the object properties needed for instance geometry
    # without actually interacting with Foundry UI in the same way that users do

    # the values being used here as the default were determined mostly by guessing
    # they should lead to acceptable results in most situations

    # there is no reason to have a conditional statement here
    # but having that somehow allows the mesh type to be reliably updated

    if obj.nwo.mesh_type_ui:
        obj.nwo.mesh_type_ui = "_connected_geometry_mesh_type_default"
        obj.nwo.poop_lighting_ui = "_connected_geometry_poop_lighting_default"
        obj.nwo.poop_pathfinding_ui = "_connected_poop_instance_pathfinding_policy_cutout"

    # there are a number of symbols used for applying specific properties to instance geometry
    # the object properties should be changed accordingly if those are in the name of the object
    # check the name for special symbols

    parse_object_name(obj.name, obj.nwo)
