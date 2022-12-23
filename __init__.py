bl_info = {
    "name":
        "Mechanyx Toolbox",
    "description":
        "Useful tools to help make things",
    "author":
        "Maki",
    "version": (1, 0, 0),
    "blender": (3, 3, 1),
    # "location": "View 3D > Tool Shelf > Mechanyx",
    "warning":
        "",
    "doc_url":
        "https://github.com/makifoxgirl/blender-mechanyx-toolbox",
    "tracker_url":
        "https://github.com/makifoxgirl/blender-mechanyx-toolbox/issues",
    "support":
        "COMMUNITY",
    "category":
        "Interface",
}

import bpy

from .operators.move_uv_map import MoveUvMap

from .panels.uv_maps_mover import UvMapsMover

classes = (
    # operators
    MoveUvMap,
    # panels
    UvMapsMover
)

# main_register, main_unregister = bpy.utils.register_classes_factory(classes)

def register():
	# main_register()
	for cls in classes:
		try:
			bpy.utils.register_class(cls)
		except Exception as e:
			print("ERROR: Failed to register class {0}: {1}".format(cls, e))

def unregister():
	# main_unregister()
	for cls in classes:
		try:
			bpy.utils.unregister_class(cls)
		except Exception as e:
			print("ERROR: Failed to unregister class {0}: {1}".format(cls, e))