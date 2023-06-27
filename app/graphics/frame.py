from config import *
import memory
import image

class UBO:


    def __init__(self):

        self.view = pyrr.matrix44.create_identity(dtype=np.float32)
        self.projection = pyrr.matrix44.create_identity(dtype=np.float32)
        self.view_projection = pyrr.matrix44.create_identity(dtype=np.float32)

class SwapChainFrame:


    def __init__(self):
        
        #swapchain
        self.image = None
        self.image_view = None
        self.depth_buffer_view = None
        self.framebuffer = None

        self.depthBuffer = None
        self.depthBufferMemory = None
        self.depthBufferView = None
        self.depthFormat = None
        self.width = None
        self.height = None

        self.commandbuffer = None

        #synchronization
        self.inFlight = None
        self.imageAvailable = None
        self.renderFinished = None

        #resources
        self.cameraData = UBO()
        self.uniformBuffer: memory.Buffer = None
        self.uniformBufferWriteLocation = None
        self.modelTransforms: np.ndarray = None
        self.modelBuffer: memory.Buffer = None
        self.modelBufferWriteLocation = None

        #resource descriptors
        self.uniformBufferDescriptor = None
        self.modelBufferDescriptor = None
        self.descriptorSet = None

    def make_descriptor_resources(self, logicalDevice, physicalDevice) -> None:

        #three matrices, each with 16 floats of 4 bytes each
        bufferSize = 3 * 16 * 4

        bufferInfo = memory.BufferInput()
        bufferInfo.logical_device = logicalDevice
        bufferInfo.physical_device = physicalDevice
        bufferInfo.memory_properties = VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT \
            | VK_MEMORY_PROPERTY_HOST_COHERENT_BIT
        bufferInfo.size = bufferSize
        bufferInfo.usage = VK_BUFFER_USAGE_UNIFORM_BUFFER_BIT

        self.uniformBuffer = memory.create_buffer(bufferInfo)

        self.uniformBufferWriteLocation = vkMapMemory(
            device = logicalDevice, 
            memory = self.uniformBuffer.buffer_memory, 
            offset = 0, size = bufferSize, flags = 0)
        
        """
            typedef struct VkDescriptorBufferInfo {
				VkBuffer        buffer;
				VkDeviceSize    offset;
				VkDeviceSize    range;
			} VkDescriptorBufferInfo;
        """
        self.uniformBufferDescriptor = VkDescriptorBufferInfo(
            buffer = self.uniformBuffer.buffer, offset = 0, range = bufferSize
        )

        self.modelTransforms = np.array(
            [pyrr.matrix44.create_identity() for _ in range(1024)],
            dtype = np.float32
        )

        bufferSize = 1024 * 16 * 4
        bufferInfo.size = bufferSize
        bufferInfo.usage = VK_BUFFER_USAGE_STORAGE_BUFFER_BIT

        self.modelBuffer = memory.create_buffer(bufferInfo)

        self.modelBufferWriteLocation = vkMapMemory(
            device = logicalDevice, 
            memory = self.modelBuffer.buffer_memory, 
            offset = 0, size = bufferSize, flags = 0)
        
        self.modelBufferDescriptor = VkDescriptorBufferInfo(
            buffer = self.modelBuffer.buffer, offset = 0, range = bufferSize
        )
    
    def make_depth_resources(self, logicalDevice, physicalDevice):
        self.depthFormat = image.find_supported_format(
            physicalDevice,
            [VK_FORMAT_D32_SFLOAT, VK_FORMAT_D32_SFLOAT_S8_UINT, VK_FORMAT_D24_UNORM_S8_UINT],
            VK_IMAGE_TILING_OPTIMAL,
            VK_FORMAT_FEATURE_DEPTH_STENCIL_ATTACHMENT_BIT
        )

        imageInfo = image.ImageCreationChunk()

        imageInfo.logicalDevice = logicalDevice
        imageInfo.physicalDevice = physicalDevice
        imageInfo.tiling = VK_IMAGE_TILING_OPTIMAL
        imageInfo.usage = VK_IMAGE_USAGE_DEPTH_STENCIL_ATTACHMENT_BIT
        imageInfo.memoryProperties = VK_MEMORY_PROPERTY_DEVICE_LOCAL_BIT
        imageInfo.width = self.width
        imageInfo.height = self.height
        imageInfo.format = self.depthFormat
        self.depthBuffer = image.make_image(imageInfo)
        self.depthBufferMemory = image.make_image_memory(imageInfo, self.depthBuffer)
        self.depth_buffer_view = image.make_image_view(logicalDevice, self.depthBuffer, self.depthFormat, VK_IMAGE_ASPECT_DEPTH_BIT) # vkImage::make_image_view(

    def write_descriptor_set(self, device):

        """
            typedef struct VkWriteDescriptorSet {
				VkStructureType                  sType;
				const void* pNext;
				VkDescriptorSet                  dstSet;
				uint32_t                         dstBinding;
				uint32_t                         dstArrayElement;
				uint32_t                         descriptorCount;
				VkDescriptorType                 descriptorType;
				const VkDescriptorImageInfo* pImageInfo;
				const VkDescriptorBufferInfo* pBufferInfo;
				const VkBufferView* pTexelBufferView;
			} VkWriteDescriptorSet;
        """

        descriptorWrites = [
            VkWriteDescriptorSet(
                dstSet = self.descriptorSet,
                dstBinding = 0,
                dstArrayElement = 0,
                descriptorType = VK_DESCRIPTOR_TYPE_UNIFORM_BUFFER,
                descriptorCount = 1,
                pBufferInfo = self.uniformBufferDescriptor
            ),
            VkWriteDescriptorSet(
                dstSet = self.descriptorSet,
                dstBinding = 1,
                dstArrayElement = 0,
                descriptorType = VK_DESCRIPTOR_TYPE_STORAGE_BUFFER,
                descriptorCount = 1,
                pBufferInfo = self.modelBufferDescriptor
            )
        ]
        
        vkUpdateDescriptorSets(
            device = device, 
            descriptorWriteCount = 2, 
            pDescriptorWrites = descriptorWrites, 
            descriptorCopyCount = 0, pDescriptorCopies = None
        )

    def destroy(self, logicalDevice):
        logicalDevice.destroyImageView(self.image_view)
        logicalDevice.destroyFramebuffer(self.framebuffer)
        logicalDevice.destroyFence(self.inFlight)
        logicalDevice.destroySemaphore(self.imageAvailable)
        logicalDevice.destroySemaphore(self.renderFinished)

        logicalDevice.unmapMemory(self.cameraData.bufferMemory)
        logicalDevice.freeMemory(self.cameraData.bufferMemory)
        logicalDevice.destroyBuffer(self.cameraData.buffer)

        logicalDevice.unmapMemory(self.modelBuffer.bufferMemory)
        logicalDevice.freeMemory(self.modelBuffer.bufferMemory)
        logicalDevice.destroyBuffer(self.modelBuffer.buffer)

        logicalDevice.destroyImage(self.depthBuffer)
        logicalDevice.freeMemory(self.depthBufferMemory)
        logicalDevice.destroyImageView(self.depth_buffer_view)