import bpy

class UvMapsMover(bpy.types.Panel):
	bl_idname = "DATA_PT_uv_maps_mover"
	bl_label = "UV Maps Mover"
	bl_context = "data"

	bl_space_type = "PROPERTIES"
	bl_region_type = "WINDOW"

	bl_order = 3
	bl_options = {"DEFAULT_CLOSED"}

	def draw(self, context):
		layout = self.layout

		up = layout.operator(
		    icon="TRIA_UP",
		    text="Move active up",
		    operator="mechanyx.move_uv_map"
		)
		up.dir = "UP"

		down = layout.operator(
		    icon="TRIA_DOWN",
		    text="Move active down",
		    operator="mechanyx.move_uv_map"
		)
		down.dir = "DOWN"
