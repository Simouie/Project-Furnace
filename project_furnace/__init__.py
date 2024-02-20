bl_info = {
    "name": "FURNACE",
    "description": "",
    "author": "Abstract Ingenuity",
    "version": (0, 9, 3),
    "blender": (3, 6, 1),
    "location": "Sidebar > Foundry > Halo 3 ASS",
    "support": 'COMMUNITY',
    "category": "Scene"
}


from . import main

def register():
    main.register()

def unregister():
    main.unregister()

if __name__ == "__main__": register()
