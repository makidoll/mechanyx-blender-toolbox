import bpy
from ..functions.sdf_texture_generator import SdfTextureGenerator

class SdfTextureGeneratorOperator(bpy.types.Operator):
	bl_idname = "mechanyx.sdf_texture_generator"
	bl_label = "Mechanyx: SDF Texture Generator"
	bl_options = {"REGISTER", "UNDO", "INTERNAL"}

	@classmethod
	def poll(cls, context):
		settings = context.scene.mechanyx_sdf_texture_generator_settings
		input_image: bpy.types.Image = settings.input_image
		return input_image != None

	def execute(self, context):
		settings = context.scene.mechanyx_sdf_texture_generator_settings

		input_image: bpy.types.Image = settings.input_image

		output_image_name: str = settings.output_image_name

		output_image: bpy.types.Image
		if bpy.data.images.find(output_image_name) > -1:
			output_image = bpy.data.images[output_image_name]
		else:
			output_image = bpy.data.images.new(
			    output_image_name,
			    width=input_image.size[0],
			    height=input_image.size[1],
			    alpha=True
			)

		SdfTextureGenerator().generate(
		    input_image=input_image,
		    output_image=output_image,
		    max_inside=settings.inside_distance,
		    max_outside=settings.outside_distance,
		    post_process_distance=settings.post_process_distance,
		)

		return {"FINISHED"}