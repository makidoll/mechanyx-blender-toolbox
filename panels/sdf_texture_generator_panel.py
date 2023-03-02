import bpy

class SdfTextureGeneratorPanel(bpy.types.Panel):
	bl_idname = "VIEW3D_PT_sdf_texture_generator"
	bl_label = "SDF Texture Generator"
	bl_icon = "OBJECT_DATA"
	bl_category = "Mechanyx"

	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"

	# PointerProperty(name="Init Image", type=bpy.types.Image)

	def draw(self, context):
		layout = self.layout

		layout.label(text="Input Image")

		if context.scene.mechanyx_sdf_texture_generator_settings.input_image == None:
			layout.template_ID(
			    context.scene.mechanyx_sdf_texture_generator_settings,
			    "input_image",
			    open="image.open"
			)
		else:
			layout.template_ID_preview(
			    context.scene.mechanyx_sdf_texture_generator_settings,
			    "input_image",
			    open="image.open",
			    hide_buttons=True
			)

		layout.separator()

		layout.use_property_split = True

		layout.prop(
		    context.scene.mechanyx_sdf_texture_generator_settings,
		    "inside_distance"
		)

		layout.prop(
		    context.scene.mechanyx_sdf_texture_generator_settings,
		    "outside_distance"
		)

		layout.prop(
		    context.scene.mechanyx_sdf_texture_generator_settings,
		    "post_process_distance"
		)

		layout.prop(
		    context.scene.mechanyx_sdf_texture_generator_settings,
		    "output_image_name"
		)

		layout.operator(
		    icon="SHADERFX",
		    text="Generate SDF Texture",
		    operator="mechanyx.sdf_texture_generator",
		)

		layout.label(
		    icon="ERROR",
		    text="Will override image with the same name",
		)

		# layout.separator()

		# output_image_name = context.scene.mechanyx_sdf_texture_generator_settings.output_image_name

		# if bpy.data.images.find(output_image_name) > -1:
		# 	aaa = bpy.data.images[output_image_name]
		# 	print(aaa)
		# 	layout.template_preview(aaa, show_buttons=False)

		# 	bpy.context.scene.mechanyx_sdf_texture_generator_settings.output_image_preview = bpy.data.images[
		# 	    output_image_name]

		# 	# 	output_image_preview_texture = bpy.data.textures[
		# 	# 	    "sdf_output_image_preview"]

		# 	# 	output_image_preview_texture.image = bpy.data.images[
		# 	# 	    output_image_name]

		# 	layout.label(text="Output Image Preview")

		# 	# 	layout.template_im

		# 	layout.template_ID_preview(
		# 	    context.scene.mechanyx_sdf_texture_generator_settings,
		# 	    output_image_preview,
		# 	    open="image.open"
		# 	)