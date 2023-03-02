bl_info = {
    "name":
        "Mechanyx Blender Toolbox",
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
        "https://github.com/makifoxgirl/mechanyx-blender-toolbox",
    "tracker_url":
        "https://github.com/makifoxgirl/mechanyx-blender-toolbox/issues",
    "support":
        "COMMUNITY",
    "category":
        "Interface",
}

import bpy

from . import addon_updater_ops

from .settings.sdf_texture_generator_settings import SdfTextureGeneratorSettings

from .operators.move_uv_map_operator import MoveUvMapOperator
from .operators.sdf_texture_generator_operator import SdfTextureGeneratorOperator

from .panels.sdf_texture_generator_panel import SdfTextureGeneratorPanel
from .panels.uv_maps_mover_panel import UvMapsMoverPanel

@addon_updater_ops.make_annotations
class MechanyxToolboxAddonPrefs(bpy.types.AddonPreferences):
	bl_idname = __name__

	auto_check_update = bpy.props.BoolProperty(
	    name="Auto-check for Update",
	    description="If enabled, auto-check for updates using an interval",
	    default=False,
	)

	updater_interval_months = bpy.props.IntProperty(
	    name="Months",
	    description="Number of months between checking for updates",
	    default=0,
	    min=0
	)

	updater_interval_days = bpy.props.IntProperty(
	    name="Days",
	    description="Number of days between checking for updates",
	    default=7,
	    min=0,
	    max=31
	)

	updater_interval_hours = bpy.props.IntProperty(
	    name="Hours",
	    description="Number of hours between checking for updates",
	    default=0,
	    min=0,
	    max=23
	)

	updater_interval_minutes = bpy.props.IntProperty(
	    name="Minutes",
	    description="Number of minutes between checking for updates",
	    default=0,
	    min=0,
	    max=59
	)

	def draw(self, context):
		# addon_updater_ops.update_settings_ui(self, context)

		layout = self.layout
		col = layout.column()
		addon_updater_ops.update_settings_ui_condensed(self, context, col)

classes = (
    # updater
    MechanyxToolboxAddonPrefs,
    # settings (property groups)
    SdfTextureGeneratorSettings,
    # operators
    MoveUvMapOperator,
    SdfTextureGeneratorOperator,
    # panels
    UvMapsMoverPanel,
    SdfTextureGeneratorPanel
)

# main_register, main_unregister = bpy.utils.register_classes_factory(classes)

def register():
	addon_updater_ops.register(bl_info)

	# main_register()
	for cls in classes:
		try:
			bpy.utils.register_class(cls)
		except Exception as e:
			print("ERROR: Failed to register class {0}: {1}".format(cls, e))

	# register all propery groups

	bpy.types.Scene.mechanyx_sdf_texture_generator_settings = bpy.props.PointerProperty(
	    type=SdfTextureGeneratorSettings
	)

def unregister():
	addon_updater_ops.unregister()

	# main_unregister()
	for cls in classes:
		try:
			bpy.utils.unregister_class(cls)
		except Exception as e:
			print("ERROR: Failed to unregister class {0}: {1}".format(cls, e))