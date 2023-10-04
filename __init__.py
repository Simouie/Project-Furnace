bl_info = {
    "name": "THREACH",
    "description": "",
    "author": "AI (Abstract Ingenuity)",
    "version": (0, 0, 0),
    "blender": (3, 6, 1),
    "location": "Sidebar > Foundry",
    "support": 'COMMUNITY',
    "category": "Scene"
}


from . import main

def register():
    main.register()

def unregister():
    main.unregister()

if __name__ == "__main__": register()
