import bpy

from . import instance_geometry
from . import materials
from . import portals
from . import glass

from bpy.types import Operator, Panel


class FURNACE_PT_Panel(Panel):

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    bl_category = "Foundry"
    bl_label = "Halo 3 ASS"

    bl_options = {"DEFAULT_CLOSED"}


    def draw(self, context):
        row = self.layout.row()
        row.operator("FURNACE.main", text="Go")


class FURNACE_Main(Operator):

    """Prepare H3 ASS for import to Reach"""

    bl_idname = "FURNACE.main"
    bl_label = "Prepare H3 ASS for import to Reach"


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

        # if the object is hidden for some reason
        # the object probably should be ignored

        if obj.hide_get(): return False

        # verify that the object has properties set up and used by Foundry
        # nothing can be done if those are not there for whatever reason

        try:

            # assume the attribute exists and try to access it to verify its existence
            # try to continue if doing this leads to an exception

            if not obj.get("nwo") and not obj.nwo: return False

        except:

            print("ERROR: Please go ensure that Foundry is installed")
            return False
        
        # ignore objects that seem to be of the wrong type

        if obj.type != "MESH": return False

        # the object meets all the requirements
        
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

            # this project is intended to work with meshes and with Foundry
            # skip to the next object if this object fails to meet the requirements

            if not self.is_valid(obj): continue

            # remove unused material slots before moving on
            
            bpy.ops.object.material_slot_remove_unused()

            # separate any geometry intended to be glass
            # two-sided geometry for levels should be separate

            if glass.has_glass(obj):

                # enter Edit Mode to work with the geometry
                # return to Object Mode for the next step

                self.select_none()
                self.select_object(obj)
                bpy.ops.object.mode_set(mode="EDIT")

                glass.separate_by_material(obj)

                bpy.ops.object.mode_set(mode="OBJECT")

            # remove unused material slots again
            
            bpy.ops.object.material_slot_remove_unused()

            # separate any geometry intended for setting up portals
            # portals are expected to be separate from other geometry

            if portals.for_portals(obj):

                # switch to Edit Mode to work with the geometry
                # return to Object Mode for the next step

                self.select_none()
                self.select_object(obj)
                bpy.ops.object.mode_set(mode="EDIT")

                portals.separate_by_material(obj)

                bpy.ops.object.mode_set(mode="OBJECT")

            # remove unused material slots again
            
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

            # for levels that are originally from Halo 3 and Halo 3: ODST
            # this is the most appropriate default mesh type

            obj.nwo.mesh_type_ui = "_connected_geometry_mesh_type_structure"

            # set the object properties according to the mesh type

            if portals.for_portals(obj):
                portals.set_object_properties(obj)

            if instance_geometry.for_instance_geometry(obj):
                instance_geometry.set_object_properties(obj)

        return {"FINISHED"}


classes = [ FURNACE_PT_Panel, FURNACE_Main ]

def register():
    for c in classes:
        bpy.utils.register_class(c)
    
def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)

if __name__ == "__main__": register()
