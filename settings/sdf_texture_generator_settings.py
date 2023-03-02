import bpy

class SdfTextureGeneratorSettings(bpy.types.PropertyGroup):
	input_image: bpy.props.PointerProperty(
	    name="Source Image", type=bpy.types.Image
	)

	inside_distance: bpy.props.IntProperty(
	    name="Inside Distance",
	    min=0,
	    default=3,
	    description=
	    "Pixel distance inside the contour that is considered fully inside."
	)

	outside_distance: bpy.props.IntProperty(
	    name="Outside Distance",
	    min=0,
	    default=3,
	    description=
	    "Pixel distance outside the contour that is considered fully outside."
	)

	post_process_distance: bpy.props.IntProperty(
	    name="Post-process Distance",
	    min=0,
	    default=0,
	    description=
	    "Pixel range in which post-processing is performed. This might improve quality close to the contour."
	)

	output_image_name: bpy.props.StringProperty(
	    name="Output Image Name",
	    default="SDF Texture",
	)
