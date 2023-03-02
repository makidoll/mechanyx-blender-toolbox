import bpy

class UvMapsMoverPanel(bpy.types.Panel):
	bl_idname = "DATA_PT_uv_maps_mover"
	bl_label = "UV Maps Mover"
	bl_context = "data"

	bl_space_type = "PROPERTIES"
	bl_region_type = "WINDOW"

	bl_order = 3  # does this even work
	bl_options = {"DEFAULT_CLOSED"}

	def draw(self, context):
		layout = self.layout

		# true will put them close together
		col = layout.column(align=False)

		up = col.operator(
		    icon="TRIA_UP",
		    text="Move active up",
		    operator="mechanyx.move_uv_map"
		)
		up.dir = "UP"

		down = col.operator(
		    icon="TRIA_DOWN",
		    text="Move active down",
		    operator="mechanyx.move_uv_map"
		)
		down.dir = "DOWN"
