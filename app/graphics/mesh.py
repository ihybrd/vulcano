from config import *

def get_pos_color_binding_description():
    """
        Get the input binding description for a
        (vec2 pos, vec3 color) vertex format
    """

    """
    typedef struct VkVertexInputBindingDescription {
        uint32_t             binding;
        uint32_t             stride;
        VkVertexInputRate    inputRate;
    } VkVertexInputBindingDescription;
    """

    floatsPerVertex = 14
    bytesPerFloat = 4
    return VkVertexInputBindingDescription(
        binding = 0, stride = floatsPerVertex * bytesPerFloat, 
        inputRate = VK_VERTEX_INPUT_RATE_VERTEX
    )

def get_pos_color_attribute_descriptions():
    """
        Get the attribute descriptions for a
        (vec2 pos, vec3 color) vertex format
    """

    """
    typedef struct VkVertexInputAttributeDescription {
        uint32_t    location;
        uint32_t    binding;
        VkFormat    format;
        uint32_t    offset;
    } VkVertexInputAttributeDescription;
    """

    bytesPerFloat = 4

    return (
        VkVertexInputAttributeDescription(
            binding = 0, location = 0,
            format = VK_FORMAT_R32G32B32_SFLOAT,
            offset = 0
        ), # vertices
        VkVertexInputAttributeDescription(
            binding = 0, location = 1,
            format = VK_FORMAT_R32G32B32_SFLOAT,
            offset = 3 * bytesPerFloat
        ), # color
        VkVertexInputAttributeDescription(
            binding = 0, location = 2,
            format = VK_FORMAT_R32G32B32_SFLOAT,
            offset = 6 * bytesPerFloat
        ), # normal
        VkVertexInputAttributeDescription(
            binding = 0, location = 3,
            format = VK_FORMAT_R32G32B32_SFLOAT,
            offset = 9 * bytesPerFloat
        ), # tangent
        VkVertexInputAttributeDescription(
            binding = 0, location = 4,
            format = VK_FORMAT_R32G32_SFLOAT,
            offset = 12 * bytesPerFloat
        ) # uv
    )