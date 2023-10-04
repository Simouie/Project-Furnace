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


    def select_none(self):

        if bpy.context.mode != "OBJECT":
            bpy.ops.object.mode_set(mode="OBJECT")

        bpy.ops.object.select_all(action="DESELECT")
        bpy.context.view_layer.objects.active = None


    def select_object(self, obj):

        if bpy.context.mode != "OBJECT":
            bpy.ops.object.mode_set(mode="OBJECT")

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
    

    def prepare_scene(self):

        # directly change the asset type to the correct type
        # without actually interacting with the Foundry UI

        bpy.data.scenes["Scene"].nwo.asset_type = "SCENARIO"

        # ensure the data of all objects are independent of each other

        bpy.ops.object.make_single_user(type="ALL", obdata=True)

        # geometry for portals might be part of any object
        # that means all the objects need to be examined

        for obj in bpy.data.objects:

            # do not go beyond this point if
            # this object is not for setting up portals

            if not portals.for_portals(obj): continue

            # switch to Edit Mode to work with the geometry
            # return to Object Mode for the next step

            self.select_none()
            self.select_object(obj)
            bpy.ops.object.mode_set(mode="EDIT")

            portals.separate_by_material(obj)

            bpy.ops.object.mode_set(mode="OBJECT")

            # when working with the materials of objects
            # unused material slots can lead to problems
            
            bpy.ops.object.material_slot_remove_unused()


    def execute(self, context):

        # to avoid some strange problems and quirks
        # there are a number of things that need to be done first

        self.prepare_scene()

        # for each object in the scene
        # set up object properties and face properties
        # according to various bits of data for the object
        # including the materials that the object uses

        for obj in bpy.data.objects:

            # this project is intended to work with meshes and with Foundry
            # skip to the next object if this object fails to meet the requirements

            if not self.is_valid(obj): continue

            # enter Edit Mode to set up face properties
            # return to Object Mode for the next step

            self.select_none()
            self.select_object(obj)
            bpy.ops.object.mode_set(mode="EDIT")

            materials.set_face_properties(obj)

            bpy.ops.object.mode_set(mode="OBJECT")
            
            if portals.for_portals(obj):
                portals.set_object_properties(obj)

            if instance_geometry.for_instance_geometry(obj):
                instance_geometry.set_object_properties(obj)

        return {"FINISHED"}


classes = [ THREACH_PT_panel, THREACH_main ]

def register():
    for c in classes:
        bpy.utils.register_class(c)
    
def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)

if __name__ == "__main__": register()
