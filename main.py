import bpy

from . import instance_geometry
from . import materials
from . import portals

from bpy.types import Operator, Panel


class THREACH_PT_panel(Panel):

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    bl_category = "Foundry"
    bl_label = "Halo 3 BSP"

    bl_options = {"DEFAULT_CLOSED"}


    def draw(self, context):
        row = self.layout.row()
        row.operator("threach.main", text="Go")


class THREACH_main(Operator):

    """Prepare H3 BSP for import to Reach"""

    bl_idname = "threach.main"
    bl_label = "Prepare H3 BSP for import to Reach"


    def enter_object_mode(self):

        # return to Object Mode

        bpy.ops.object.mode_set(mode="OBJECT")

        # reset selection before moving on

        bpy.ops.object.select_all(action="DESELECT")
        bpy.context.view_layer.objects.active = None


    def enter_edit_mode(self, obj):

        # switch to Object Mode if not already in that mode

        if bpy.context.mode != "OBJECT": 
            bpy.ops.object.mode_set(mode="OBJECT")
        
        # reset selection before moving on

        bpy.ops.object.select_all(action="DESELECT")
        bpy.context.view_layer.objects.active = None

        # select object as active object

        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj

        # switch to Edit Mode to set up face properties

        bpy.ops.object.mode_set(mode="EDIT")


    def process(self, obj):

        # enter Edit Mode to do various things with the geometry
        # return to Object Mode after that stuff gets done

        self.enter_edit_mode(obj)

        materials.set_face_properties(obj)
        portals.set_object_properties(obj)

        self.enter_object_mode()

        if instance_geometry.is_instance_geometry(obj):
            instance_geometry.set_object_properties(obj)

    
    def prepare(self, obj):

        # set the mesh type to the default mesh type for scenarios
        # assuming the current mesh type may not be correct 

        obj.nwo.mesh_type_ui = bpy.data.scenes["Scene"].nwo.default_mesh_type_ui

        # reset selection before moving on

        bpy.ops.object.select_all(action="DESELECT")
        bpy.context.view_layer.objects.active = None

        # select object as active object

        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj


    def is_valid(self, obj): 

        # verify that the object has properties set up and used by Foundry
        # nothing can be done if those are not there for whatever reason

        try:

            # assume the attribute exists and try to access it to verify its existence
            # try to continue if doing this leads to an exception

            if not obj.get("nwo") and not obj.nwo: return False

        except:

            print("ERROR: Please go ensure that Foundry is installed")
            return False

        if obj.type != "MESH": return False
        
        return True
    

    def execute(self, context):

        # directly change the asset type to the correct type
        # without actually interacting with the Foundry UI

        bpy.data.scenes["Scene"].nwo.asset_type = "SCENARIO"

        # for each object in the scene
        # set up object properties and face properties
        # according to various bits of data for the object
        # including the materials that the object uses

        for obj in bpy.data.objects:

            # this project is intended to work with meshes and with Foundry
            # skip to the next object if this object fails to meet the requirements

            if not self.is_valid(obj): continue

            self.prepare(obj)
            self.process(obj)

        return {"FINISHED"}


classes = [ THREACH_PT_panel, THREACH_main ]

def register():
    for c in classes:
        bpy.utils.register_class(c)
    
def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)

if __name__ == "__main__": register()
