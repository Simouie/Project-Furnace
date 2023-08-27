import bpy
import math


def transfer_settings(a, b):
    
    b.Material_Lighting_Enabled = True
    b.Lightmap_Settings_Enabled = True

    b.Material_Lighting_Emissive_Color = a.color
    b.Material_Lighting_Emissive_Power = a.power
    b.Material_Lighting_Emissive_Focus = a.emissive_focus
    b.Material_Lighting_Emissive_Quality = a.quality

    if a.attenuation_enabled:
        b.Material_Lighting_Attenuation_Falloff = a.falloff_distance
        b.Material_Lighting_Attenuation_Cutoff = a.cutoff_distance

    b.Material_Lighting_Emissive_Per_Unit = a.power_per_unit_area
    b.Material_Lighting_Use_Shader_Gel = a.use_shader_gel

    b.Lightmap_Translucency_Tint_Color = a.two_sided_transparent_tint
    b.Lightmap_Additive_Transparency = a.additive_transparency.hsv[2]

    b.Lightmap_Resolution_Scale = math.ceil(a.lightmap_res)
    
    
def separate_materials(obj):

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

    # separate mesh by material
    # there will be multiple objects if there are multiple materials

    bpy.ops.mesh.separate(type="MATERIAL") 

    # return to Object Mode

    bpy.ops.object.mode_set(mode="OBJECT", toggle=False)

    # reset selection before moving on
    
    bpy.ops.object.select_all(action="DESELECT")
    objects.active = None


def main():

    # separate each mesh by material
    # each mesh should have one material

    for obj in bpy.data.objects:

        # proceed only if object is mesh

        if obj.type != "MESH": continue

        # separate mesh into one or more objects
        # according to material assigned to geometry

        separate_materials(obj)

    # transfer settings used for lighting from material to object
    # this step requires all meshes to be fully separated by material

    for obj in bpy.data.objects:

        # proceed only if object is mesh
        
        if obj.type != "MESH": continue

        # do not proceed if there are no materials

        if len(obj.material_slots) < 1: continue

        # do not proceed if object is not for Halo

        if obj.get("nwo") == None: continue

        # object should have one material

        material = obj.material_slots[0].material

        # copy values from material to object

        transfer_settings(material.ass_jms, obj.nwo)
        
main()
