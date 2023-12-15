import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


class CommonPlottingParams:
	def __init__(self, size_in_inches=(9, 4), show_labels=False, title=" "):
		self.fig = plt.figure()
		self.fig.set_size_inches(size_in_inches)
		self.plotting_axes = plt.axes(projection='3d')
		self.title = title
		self.show_labels = show_labels
		self.size_in_inches = size_in_inches


class RotationPlotter:
	def __init__(self, plotting_params, origin=(0, 0, 0), world_axes_size=4, rotated_axes_scale=3, plotting_axes_range=6):
		self.plotting_params = plotting_params
		self.origin = origin
		self.world_axes_size = world_axes_size
		self.plotting_axes_range = plotting_axes_range
		self.colours = list(mcolors.TABLEAU_COLORS)
		self.rotated_axes_scale = np.diag((1, 1, 1)) * rotated_axes_scale


	def plot_multiple_rotation_matrices(self, rotations):
		"""
		Plots multiple rotation matrices in a single figure.
		@param rotations: A dictionary of 3x3 rotation matrices and their names.
		@return: None
		"""
		subplot_rows = 1
		subplot_columns = len(rotations)
		self.plotting_params.fig.clear()
		for i, rotation in enumerate(rotations.items()):
			current_subplot = i + 1
			self.plotting_params.plotting_axes = self.plotting_params.fig.add_subplot(subplot_rows,
																			subplot_columns,
																			current_subplot,
																			projection='3d')
			self.plotting_params.title = rotation[0]
			self.plot_rotation_matrix_in_world_frame(rotation[1])

	def plot_rotation_matrix_and_vectors_in_world_frame(self, rotation, vectors):
		"""
		Plots a single rotation matrix and a tuple of vectors in a stationary world frame 
		@param rotation: A 3x3 rotation matrix.
		@param vectors: A dictionary of vector name pairs.
		@return: None
		"""
		self.plot_rotation_matrix_in_world_frame(rotation)
		for name, vector in vectors.items():
			self.plot_vector(self.plotting_params.plotting_axes, self.origin, vector,  colour=self.select_colour(), name=name)

	def plot_rotation_matrix_in_world_frame(self, rotation_matrix):
		"""
		Plots a single rotation matrix and stationary world axes witin in a single figure.
		@param rotation_matrix: A 3x3 rotation matrix.
		@return: None
		"""
		self.plot_world_frame()
		self.plot_scaled_rotation_matrix(rotation_matrix)
		plt.show()

	def plot_scaled_rotation_matrix(self, rotation_matrix):
		scaled_rotation_matrix = rotation_matrix @ self.rotated_axes_scale
		x_axis = scaled_rotation_matrix[:, 0]
		y_axis = scaled_rotation_matrix[:, 1]
		z_axis = scaled_rotation_matrix[:, 2]
		self.plot_vector(self.plotting_params.plotting_axes, self.origin, x_axis, colour='r', name='x-rot')
		self.plot_vector(self.plotting_params.plotting_axes, self.origin, y_axis, colour='g', name='y-rot')
		self.plot_vector(self.plotting_params.plotting_axes, self.origin, z_axis, colour='b', name='z-rot')


	def plot_world_frame(self):
		self.set_world_frame_limits(self.plotting_params.plotting_axes)
		amount_of_plotting_data = 100
		bunch_of_zeros = np.zeros(amount_of_plotting_data)
		world_axes = [np.linspace(self.origin[i], self.world_axes_size, amount_of_plotting_data) for i in range(3)]

		self.plotting_params.plotting_axes.plot(world_axes[0], bunch_of_zeros, bunch_of_zeros, "r--")
		self.plotting_params.plotting_axes.plot(bunch_of_zeros, world_axes[1], bunch_of_zeros, "g--")
		self.plotting_params.plotting_axes.plot(bunch_of_zeros, bunch_of_zeros, world_axes[2], "b--")

		self.plotting_params.plotting_axes.set_xlabel('X world')
		self.plotting_params.plotting_axes.set_ylabel('Y world')
		self.plotting_params.plotting_axes.set_zlabel('Z world')
		plt.title(self.plotting_params.title)

	def set_world_frame_limits(self, plotting_axes):
		half_range = self.plotting_axes_range / 2
		limits = [(x - half_range, x + half_range) for x in self.origin]
		plotting_axes.set_xlim([limits[0][0], limits[0][1]])
		plotting_axes.set_ylim([limits[1][0], limits[1][1]])
		plotting_axes.set_zlim([limits[2][0], limits[2][1]])
	
	def plot_vector(self, plotting_axes, start_coordinates, end_coordinates, colour="m", name="vector"):
		plotting_axes.quiver(*start_coordinates, *end_coordinates, color=colour, label=name)
		if self.plotting_params.show_labels:
			plt.legend()

	def select_colour(self):
		colour = self.colours[0]
		self.colours = self.colours[1:]
		if len(self.colours) < 1:
			self.colours = list(mcolors.TABLEAU_COLORS)
		return colour

	
def Rx(angle, degrees=False):
	if degrees:
		angle = np.deg2rad(angle)
	return np.array([[1., 0., 0.], [0., np.cos(angle), -np.sin(angle)], [0., np.sin(angle), np.cos(angle)]])


def Ry(angle, degrees=False):
	if degrees:
		angle = np.deg2rad(angle)
	return np.array([[np.cos(angle), 0., np.sin(angle)], [0., 1., 0.], [-np.sin(angle), 0., np.cos(angle)]])


def Rz(angle, degrees=False):
	if degrees:
		angle = np.deg2rad(angle)
	return np.array([[np.cos(angle), -np.sin(angle), 0.], [np.sin(angle), np.cos(angle), 0.], [0., 0., 1.]])

