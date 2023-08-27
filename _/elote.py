import bpy

from bpy.props import BoolProperty, PointerProperty
from bpy.types import Operator, Panel, PropertyGroup


bl_info = {
    "name": "Halo 3 Objects and Materials Extension for Foundry",
    "description": "Process symbols and values into properties usable for GR2 workflow",
    "author": "Abstract Ingenuity (AI)",
    "version": (0, 0, 0),
    "location": "Sidebar > Foundry",
    "support": "COMMUNITY",
    "category": "Scene",
}


class THREACH_ResetFaceProperties(Operator):

    """Lorem ipsum"""

    bl_idname = "threach_objects_materials.reset_face_properties"
    bl_label = "Lorem ipsum"

    filename_ext = ""


    def execute(self, context):

        for obj in bpy.data.objects:
            if obj.type != "MESH": continue
            if obj.data.get("nwo") == None: continue
            obj.data.nwo.face_props.clear()

        return {"FINISHED"}


class THREACH_Settings(PropertyGroup):
    reset_face_properties: BoolProperty(default=False)


class THREACH_PT_Panel(Panel):

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    bl_category = "Foundry"
    bl_label = "Test"

    bl_options = {"DEFAULT_CLOSED"}


    def draw(self, context):

        settings = context.scene.threach_objects_materials
        layout = self.layout

        row = layout.row()
        row.label(text="Reset face properties")

        reset = settings.reset_face_properties
        boolean_text = { True: "Yes", False: "No" }

        row = layout.row()
        row.prop(settings, "reset_face_properties", toggle=1, text=boolean_text[reset])
        
        if reset:
            row = layout.row()
            row.operator("threach_objects_materials.reset_face_properties", text="Reset")


classes = [ 
    THREACH_ResetFaceProperties,
    THREACH_Settings, 
    THREACH_PT_Panel
]


def register():

    for c in classes:
        bpy.utils.register_class(c)

    bpy.types.Scene.threach_objects_materials = PointerProperty(
        type=THREACH_Settings, name="THREACH_Settings",
        description="Lorem ipsum"
    )

def unregister():

    del bpy.types.Scene.threach_objects_materials

    for c in classes:
        bpy.utils.unregister_class(c)

if __name__ == "__main__": register()
