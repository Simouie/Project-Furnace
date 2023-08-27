import bpy


def show_message(text="", title="", icon="INFO"):

    def draw(self, context):
        self.layout.label(text=text)

    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)


def set_flags(flags):

    ass_to_nwo = {
        "ladder": "ladder",
        "slip_surface": "slip_surface",
        "decal_offset": "decal_offset",
        "group_transparents_by_plane": "group_transparents_by_plane",
        "no_shadow": "no_shadow",
        "ignored_by_lightmaps": "no_lightmap",
        "portal_vis_blocker": "no_pvs",
    }

    for k, v in ass_to_nwo.items():
        if getattr(flags, k): bpy.ops.nwo.face_layer_add_flags(options=v)


def set_face_modes(flags):

    ass_to_nwo = {
        "render_only": "_connected_geometry_face_mode_render_only",
        "collision_only": "_connected_geometry_face_mode_collision_only",
        "sphere_collision_only": "_connected_geometry_face_mode_sphere_collision_only",
        "shadow_only": "_connected_geometry_face_mode_shadow_only",
        "lightmap_only": "_connected_geometry_face_mode_lightmap_only",
        "breakable": "_connected_geometry_face_mode_breakable"
    }

    for k, v in ass_to_nwo.items():
        if getattr(flags, k): bpy.ops.nwo.face_layer_add_face_mode(options=v)


def set_face_layers(flags):

    ass_to_nwo = {
        "two_sided": "two_sided",
        "precise": "precise_position"
    }

    for k, v in ass_to_nwo.items():
        if getattr(flags, k): bpy.ops.nwo.face_layer_add(options=v)


def set_values_portal(obj, flags):

    ass_to_nwo = {
        "ai_deafening": "portal_ai_deafening_ui",
        "blocks_sound": "portal_blocks_sounds_ui",
        "portal_door": "portal_is_door_ui",
    }

    obj.mesh_type_ui = "_connected_geometry_mesh_type_plane"
    obj.plane_type_ui = "_connected_geometry_plane_type_portal"
    obj.portal_type_ui = "_connected_geometry_portal_type_two_way"

    # if flags.two_sided:
    #     obj.portal_type_ui = "_connected_geometry_portal_type_two_way"

    if flags.portal_1_way:
        obj.portal_type_ui = "_connected_geometry_portal_type_one_way"

    for k, v in ass_to_nwo.items():
        setattr(obj, v, getattr(flags, k))


def set_values_sky_material(name, mesh):

    bpy.ops.nwo.face_layer_add(options="_connected_geometry_face_type_sky")

    suffix = name.split("+sky")[1]

    if suffix.isdigit():
        mesh.face_props[-1].sky_permutation_index_ui = int(suffix)


def copy_values(material, obj):

    if material.name.startswith("+sky"):
        set_values_sky_material(material.name, obj.data.nwo)
        return
    
    if material.name.startswith("+seamsealer"):
        bpy.ops.nwo.face_layer_add(options="_connected_geometry_face_type_seam_sealer")
        return
    
    if material.name.startswith("+portal"):
        set_values_portal(obj.nwo, material.ass_jms)
        return
    
    if material.ass_jms.fog_plane: 
        obj.mesh_type_ui = "_connected_geometry_mesh_type_plane"
        obj.plane_type_ui = "_connected_geometry_plane_type_planar_fog_volume"
        return
    
    if material.ass_jms.water_surface: 
        obj.mesh_type_ui = "_connected_geometry_mesh_type_plane"
        obj.plane_type_ui = "_connected_geometry_plane_type_water_surface"
        return

    if material.ass_jms.material_effect.strip() != "":
        bpy.ops.nwo.face_layer_add(options="face_global_material") 
        obj.data.nwo.face_props[-1].face_global_material_ui = material.ass_jms.material_effect
    
    set_face_layers(material.ass_jms)
    set_face_modes(material.ass_jms)
    set_flags(material.ass_jms)

    
def transfer_settings(obj):

    # if not already in Object Mode
    # tell user to switch to Object Mode

    if bpy.context.mode != "OBJECT":
        show_message(text="Please switch to Object Mode first!")
        return

    # set up variable for better clarity
    
    objects = bpy.context.view_layer.objects

    # reset selection before moving on
    
    bpy.ops.object.select_all(action="DESELECT")
    objects.active = None

    # select object as active object
    
    obj.select_set(True)
    objects.active = obj

    # switch to Edit Mode to work on mesh
    
    bpy.ops.object.mode_set(mode="EDIT", toggle=False)

    # copy values from each material to object

    for index, slot in enumerate(obj.material_slots):

        # move on if there is no material in material slot
        
        if slot.material == None: continue

        # directly setting active material seems to be incorrect
        # selecting material in user interface changes active material index

        obj.active_material_index = index
        bpy.ops.object.material_slot_select()

        # copy values from active material to object
        
        copy_values(slot.material, obj)

        # reset selection before moving on

        bpy.ops.mesh.select_all(action="DESELECT")
        
    # return to Object Mode

    bpy.ops.object.mode_set(mode="OBJECT", toggle=False)

    # reset selection before moving on
    
    bpy.ops.object.select_all(action="DESELECT")
    objects.active = None


def main():

    for obj in bpy.data.objects:

        # proceed only if object is mesh
        
        if obj.type != "MESH": continue

        # do not proceed if there are no materials

        if len(obj.material_slots) < 1: continue

        # do not proceed if object is not for Halo

        if obj.get("nwo") == None: continue

        # copy values from each material to object

        transfer_settings(obj)
        
main()
