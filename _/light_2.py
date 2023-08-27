import bpy


def show_message(text="", title="", icon="INFO"):

    def draw(self, context):
        self.layout.label(text=text)

    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)


def copy_values(a, b):

    bpy.ops.nwo.face_layer_add(options="emissive")

    b.face_props[-1].material_lighting_emissive_color_ui = a.color
    b.face_props[-1].material_lighting_emissive_power_ui = a.power
    b.face_props[-1].material_lighting_emissive_quality_ui = a.quality
    b.face_props[-1].material_lighting_emissive_focus_ui = a.emissive_focus
    
    if a.attenuation_enabled:
        b.face_props[-1].material_lighting_attenuation_falloff_ui = a.falloff_distance
        b.face_props[-1].material_lighting_attenuation_cutoff_ui = a.cutoff_distance

    b.face_props[-1].material_lighting_use_shader_gel_ui = a.use_shader_gel
    b.face_props[-1].material_lighting_emissive_per_unit_ui = a.power_per_unit_area

    bpy.ops.nwo.face_layer_add_lightmap(options="lightmap_resolution_scale")

    b.face_props[-1].lightmap_resolution_scale_ui = round(a.lightmap_res * 3)

    if a.additive_transparency.hsv[2] > 0.0:
        
        bpy.ops.nwo.face_layer_add_lightmap(options="lightmap_additive_transparency")
        b.face_props[-1].lightmap_additive_transparency_ui = a.additive_transparency
        
    if a.two_sided_transparent_tint.hsv[2] > 0.0:

        bpy.ops.nwo.face_layer_add_lightmap(options="lightmap_translucency_tint_color")
        b.face_props[-1].lightmap_translucency_tint_color_ui = a.two_sided_transparent_tint

    
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
        
        copy_values(slot.material.ass_jms, obj.data.nwo)

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
