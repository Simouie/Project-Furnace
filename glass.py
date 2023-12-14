import bpy


def has_glass(obj):

    # portals in Halo are set up using meshes
    # abort if the object is not able to have meshes

    if not obj.type == "MESH": return False
        
    # if one of the materials seems to be two-sided in some way
    # assume the object has glass or something similar

    for slot in obj.material_slots:

        # go to the next slot if
        # the slot has no material
        # the material is not a material for Halo

        if not slot.material: continue
        if not slot.material.get("ass_jms"): continue

        # if material is two-sided or transparent and two-sided
        # the material probably is glass or something similar

        if is_two_sided(slot.material): return True

    return False


def is_two_sided(material):

    if "glass" in material.name:
        if material.ass_jms.two_sided: return True
        if material.ass_jms.transparent_2_sided: return True

    return False


def separate_selection():

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

    # if there are less than two materials
    # there is no need to do anything here

    if len(obj.material_slots) < 2: return

    # reset selection before moving on

    bpy.ops.mesh.select_all(action="DESELECT")

    # select the geometry not intended to be glass or something similar
    # separate all that geometry from everything else

    for index, slot in enumerate(obj.material_slots):

        # do not select any geometry by the material if
        # the slot has no material
        # the material is not a material meant for Halo
    
        if not slot.material: continue
        if not slot.material.get("ass_jms"): continue

        # do not select any geometry by the material if
        # the material is intended to be two-sided

        if is_two_sided(slot.material): continue

        # directly setting the active material seems to be incorrect
        # selecting material in user interface changes the active material index
        # setting the index seems to be the correct way to set the active material

        obj.active_material_index = index
        bpy.ops.object.material_slot_select()
    
    separate_selection()

    # reset selection before moving on

    bpy.ops.mesh.select_all(action="DESELECT")

    # separate everything else by material

    bpy.ops.mesh.separate(type="MATERIAL")
