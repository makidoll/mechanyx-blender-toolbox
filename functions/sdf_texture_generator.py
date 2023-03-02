import bpy
import math
import numpy as np
import numpy.typing as npt
import time

def clamp(num, min_value, max_value):
	return max(min(num, max_value), min_value)

def clamp01(num):
	return clamp(num, 0, 1)

class Pixel:
	alpha: float = 0
	distance: float = 0
	gradientX: float = 0
	gradientY: float = 0
	dX: int = 0
	dY: int = 0

	def gradientNormalize(self):
		mag = math.sqrt(
		    self.gradientX * self.gradientX + self.gradientY * self.gradientY
		)
		if mag > 0:
			self.gradientX = self.gradientX / mag
			self.gradientY = self.gradientY / mag

class SdfTextureGenerator:
	width: int
	height: int
	pixels: npt.NDArray

	def compute_edge_gradients(self):
		sqrt2 = math.sqrt(2)
		for y in range(1, self.height - 1):
			for x in range(1, self.width - 1):
				p: Pixel = self.pixels[x, y]
				if p.alpha > 0 and p.alpha < 1:
					# estimate gradient of edge pixel using surrounding pixels
					g = (
					    -self.pixels[x - 1, y - 1].alpha -
					    self.pixels[x - 1, y + 1].alpha +
					    self.pixels[x + 1, y - 1].alpha +
					    self.pixels[x + 1, y + 1].alpha
					)

					p.gradientX = g + (
					    self.pixels[x + 1, y].alpha -
					    self.pixels[x - 1, y].alpha
					) * sqrt2

					p.gradientY = g + (
					    self.pixels[x, y + 1].alpha -
					    self.pixels[x, y - 1].alpha
					) * sqrt2

					p.gradientNormalize()

	def approximate_edge_delta(self, gx: float, gy: float, a: float):
		# (gx, gy) can be either the local pixel gradient or the direction to the pixel

		if gx == 0 or gy == 0:
			# linear function is correct if both gx and gy are zero
			# and still fair if only one of them is zero
			return 0.5 - a

		# normalize (gx, gy)
		length = math.sqrt(gx * gx + gy * gy)
		gx = gx / length
		gy = gy / length

		# reduce symmetrical equation to first octant only
		# gx >= 0, gy >= 0, gx >= gy
		gx = math.fabs(gx)
		gy = math.fabs(gy)
		if gx < gy:
			temp = gx
			gx = gy
			gy = temp

		# compute delta
		a1 = 0.5 * gy / gx

		if a < a1:
			# 0 <= a < a1
			return 0.5 * (gx + gy) - math.sqrt(2 * gx * gy * a)

		if a < (1 - a1):
			# a1 <= a <= 1 - a1
			return (0.5 - a) * gx

		# 1-a1 < a <= 1
		return -0.5 * (gx + gy) + math.sqrt(2 * gx * gy * (1 - a))

	def update_distance(self, p: Pixel, x: int, y: int, oX: int, oY: int):
		neighbor: Pixel = self.pixels[x + oX, y + oY]
		closest: Pixel = self.pixels[x + oX - neighbor.dX, y + oY - neighbor.dY]

		if closest.alpha == 0 or closest == p:
			# neighbor has no closest yet
			# or neighbor's closest is p itself
			return

		dX = neighbor.dX - oX
		dY = neighbor.dY - oY

		distance = math.sqrt(dX * dX + dY * dY) + self.approximate_edge_delta(
		    dX, dY, closest.alpha
		)

		if distance < p.distance:
			p.distance = distance
			p.dX = dX
			p.dY = dY

	def generate_distance_transform(self):
		# perform anti-aliased Euclidean distance transform

		width = self.pixels.shape[0]
		height = self.pixels.shape[1]

		# initialize distances
		for y in range(0, height):
			for x in range(0, width):
				p: Pixel = self.pixels[x, y]
				p.dX = 0
				p.dY = 0

				if p.alpha <= 0:
					# outside
					p.distance = 1000000

				elif p.alpha < 1:
					# on the edge
					p.distance = self.approximate_edge_delta(
					    p.gradientX, p.gradientY, p.alpha
					)

				else:
					# inside
					p.distance = 0

		# perform 8SSED (eight-points signed sequential Euclidean distance transform)
		# scan up
		for y in range(1, height):
			# |P.
			# |XX
			p: Pixel = self.pixels[0, y]
			if p.distance > 0:
				self.update_distance(p, 0, y, 0, -1)
				self.update_distance(p, 0, y, 1, -1)

			# -->
			# XP.
			# XXX
			for x in range(1, width - 1):
				p: Pixel = self.pixels[x, y]
				if p.distance > 0:
					self.update_distance(p, x, y, -1, 0)
					self.update_distance(p, x, y, -1, -1)
					self.update_distance(p, x, y, 0, -1)
					self.update_distance(p, x, y, 1, -1)

			# XP|
			# XX|
			p: Pixel = self.pixels[width - 1, y]
			if p.distance > 0:
				self.update_distance(p, width - 1, y, -1, 0)
				self.update_distance(p, width - 1, y, -1, -1)
				self.update_distance(p, width - 1, y, 0, -1)

			# <--
			# .PX
			for x in range(width - 2, -1, -1):
				p: Pixel = self.pixels[x, y]
				if p.distance > 0:
					self.update_distance(p, x, y, 1, 0)

		# scan down
		for y in range(height - 2, -1, -1):
			# XX|
			# .P|
			p: Pixel = self.pixels[width - 1, y]
			if p.distance > 0:
				self.update_distance(p, width - 1, y, 0, 1)
				self.update_distance(p, width - 1, y, -1, 1)

			# <--
			# XXX
			# .PX
			for x in range(width - 2, 0, -1):
				p: Pixel = self.pixels[x, y]
				if p.distance > 0:
					self.update_distance(p, x, y, 1, 0)
					self.update_distance(p, x, y, 1, 1)
					self.update_distance(p, x, y, 0, 1)
					self.update_distance(p, x, y, -1, 1)

			# |XX
			# |PX
			p: Pixel = self.pixels[0, y]
			if p.distance > 0:
				self.update_distance(p, 0, y, 1, 0)
				self.update_distance(p, 0, y, 1, 1)
				self.update_distance(p, 0, y, 0, 1)

			# -->
			# XP.
			for x in range(1, width):
				p: Pixel = self.pixels[x, y]
				if p.distance > 0:
					self.update_distance(p, x, y, -1, 0)

	def post_process(self, max_distance: int):
		# adjust distances near edges based on the local edge gradient
		for y in range(0, self.height):
			for x in range(0, self.width):
				p: Pixel = self.pixels[x, y]

				if (p.dX == 0 and p.dY == 0) or p.distance >= max_distance:
					# ignore edge, inside, and beyond max distance
					continue

				dX = p.dX
				dY = p.dY

				closest: Pixel = self.pixels[x - p.dX, y - p.dY]
				gX = closest.gradientX
				gY = closest.gradientY

				if gX == 0 and gY == 0:
					# ignore unknown gradients (inside)
					continue

				# compute hit point offset on gradient inside pixel
				df = self.approximate_edge_delta(gX, gY, closest.alpha)
				t = dY * gX - dX * gY
				u = -df * gX + t * gY
				v = -df * gY - t * gX

				# use hit point to compute distance
				if math.fabs(u) <= 0.5 and math.fabs(v) <= 0.5:
					p.distance = math.sqrt(
					    (dX + u) * (dX + u) + (dY + v) * (dY + v)
					)

	def generate(
	    self, input_image: bpy.types.Image, output_image: bpy.types.Image,
	    max_inside: int, max_outside: int, post_process_distance: int
	):
		# rewritten from SDFTextureGenerator.cs
		# https://assetstore.unity.com/packages/tools/utilities/sdf-toolkit-free-50191

		# although it reads black and white pixels and outputs black and white pixels

		# global start_time
		# start_time = time.time()

		def benchmark_since_last(type: str):
			# global start_time
			# print(
			#     type + ": " + str(round(time.time() - start_time, 2)) +
			#     " seconds"
			# )
			# start_time = time.time()
			pass

		self.width = input_image.size[0]
		self.height = input_image.size[1]

		source_pixels = np.array(input_image.pixels)

		def read_source_pixel(x: int, y: int) -> float:
			i = (y * self.width + x) * input_image.channels
			r = source_pixels[i + 0]
			g = source_pixels[i + 1]
			b = source_pixels[i + 2]
			return (r + g + b) / 3

		self.pixels = np.zeros([self.width, self.height], dtype=np.object)

		output_pixels = [0] * self.width * self.height * 4

		def set_output_pixel(x: int, y: int, value: float):
			i = (y * self.width + x) * 4
			output_pixels[i + 0] = value
			output_pixels[i + 1] = value
			output_pixels[i + 2] = value
			output_pixels[i + 3] = 1

		def get_output_pixel(x: int, y: int):
			return output_pixels[(y * self.width + x) * 4]

		for y in range(0, self.height):
			for x in range(0, self.width):
				self.pixels[x, y] = Pixel()

		benchmark_since_last("init")

		if max_inside > 0:
			for y in range(0, self.height):
				for x in range(0, self.width):
					self.pixels[x, y].alpha = 1 - read_source_pixel(x, y)
			benchmark_since_last("max_inside, read_source_pixels")

			self.compute_edge_gradients()
			benchmark_since_last("max_inside, compute_edge_gradients")

			self.generate_distance_transform()
			benchmark_since_last("max_inside, generate_distance_transform")

			if post_process_distance > 0:
				self.post_process(post_process_distance)
				benchmark_since_last("max_inside, post_process")

			scale = 1 / max_inside
			for y in range(0, self.height):
				for x in range(0, self.width):
					alpha = clamp01(self.pixels[x, y].distance * scale)
					set_output_pixel(x, y, alpha)

			benchmark_since_last("max_inside, set_output_pixels")

		if max_outside > 0:
			for y in range(0, self.height):
				for x in range(0, self.width):
					self.pixels[x, y].alpha = read_source_pixel(x, y)
			benchmark_since_last("max_outside, read_source_pixels")

			self.compute_edge_gradients()
			benchmark_since_last("max_outside, compute_edge_gradients")

			self.generate_distance_transform()
			benchmark_since_last("max_outside, generate_distance_transform")

			if post_process_distance > 0:
				self.post_process(post_process_distance)
				benchmark_since_last("max_outside, post_process")

			scale = 1 / max_outside
			if max_inside > 0:
				for y in range(0, self.height):
					for x in range(0, self.width):
						alpha = 0.5 + (
						    get_output_pixel(x, y) -
						    clamp01(self.pixels[x, y].distance * scale)
						) * 0.5
						set_output_pixel(x, y, alpha)
			else:
				for y in range(0, self.height):
					for x in range(0, self.width):
						alpha = clamp01(1 - self.pixels[x, y].distance * scale)
						set_output_pixel(x, y, alpha)

			benchmark_since_last("max_outside, set_output_pixels")

		# write pixels

		if output_image.size[0] != self.width or output_image.size[
		    1] != self.height:
			# should we set pixels to null first? dont want to unnecessarily scale
			output_image.scale(self.width, self.height)

		output_image.pixels[:] = output_pixels
		output_image.pack()
		output_image.reload()

		benchmark_since_last("write pixels")
