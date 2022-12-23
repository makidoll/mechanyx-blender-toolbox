import bpy

class MoveUvMap(bpy.types.Operator):
	bl_idname = "mechanyx.move_uv_map"
	bl_label = "Mechanyx: Move UV map"
	bl_options = {"REGISTER", "UNDO", "INTERNAL"}

	dir: bpy.props.EnumProperty(
	    name="Dir",
	    default="DOWN",
	    items=[
	        ("UP", "Up", ""),
	        ("DOWN", "Down", ""),
	    ]
	)

	def execute(self, context):
		obj = context.active_object
		uv_layers = obj.data.uv_layers

		if len(uv_layers) == 8:
			raise Exception("Can't move UV map because there are 8 maximum")

		def move_to_bottom(index):

			if index == len(uv_layers) - 1:
				# already at bottom
				return

			if index < 0 or index >= len(uv_layers) - 1:
				raise Exception(
				    "Can't move non-existent UV index " + str(index) +
				    " to bottom"
				)

			uv_layers.active_index = index
			uv_name = uv_layers.active.name

			# clone active
			new_uv = uv_layers.new(do_init=True)
			if new_uv == None:
				return
			new_uv_name = new_uv.name

			# delete old uv map
			uv_layers.remove(uv_layers[index])

			# rename new map now at the bottom
			uv_layers[new_uv_name].name = uv_name

		if self.dir == "UP":
			# dont do anything if already at top
			if uv_layers.active_index == 0:
				return {"FINISHED"}

			# 0      0 ____ 0  0  0  0
			# 1  .-> 2 ____ 1. 2  2  2
			# 2 -`   1 ____ 2  3. 4. 1
			# 3      3 ____ 3  4  1  3
			# 4      4 ____ 4  1  3  4

			start_index = uv_layers.active_index

			move_to_bottom(start_index - 1)

			to_move = len(uv_layers) - (start_index + 1)
			for _ in range(0, to_move):
				move_to_bottom(start_index)

			# update active
			uv_layers.active_index = start_index - 1

		elif self.dir == "DOWN":
			# dont do anything if already at bottom
			if uv_layers.active_index == len(uv_layers) - 1:
				return {"FINISHED"}

			# 0      0 ____ 0  0  0  0
			# 1 -.   2 ____ 1. 2  2  2
			# 2  `-> 1 ____ 2  3. 4. 1
			# 3      3 ____ 3  4  1  3
			# 4      4 ____ 4  1  3  4

			start_index = uv_layers.active_index

			move_to_bottom(start_index)

			to_move = len(uv_layers) - (start_index + 2)
			for _ in range(0, to_move):
				move_to_bottom(start_index + 1)

			# update active
			uv_layers.active_index = start_index + 1

		else:
			raise Exception("Can't move UV in direction: " + self.dir)

		return {"FINISHED"}