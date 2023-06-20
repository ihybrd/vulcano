from vulkan import *

"""
 Statically linking the prebuilt header from the lunarg sdk will load
 most functions, but not all.
 
 Functions can also be dynamically loaded, using the call
 
 PFN_vkVoidFunction vkGetInstanceProcAddr(
    VkInstance                                  instance,
    string                                      pName);

 or

 PFN_vkVoidFunction vkGetDeviceProcAddr(
	VkDevice                                    device,
	string                                      pName);

	We will look at this later, once we've created an instance and device.
"""

import glfw
import glfw.GLFW as GLFW_CONSTANTS
import numpy as np
import pyrr
import sys
import os

#----- Mesh Types ----#
TRIANGLE = 0
SQUARE = 1
STAR = 2

# detect os
is_darwin = True if sys.platform == 'darwin' else False

# add graphics dir to the sys path
graph_dir = os.path.dirname(__file__)+"/"
sys.path.append(graph_dir)