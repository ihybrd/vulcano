#version 450

layout(location = 0) in vec3 vertexPosition;
layout(location = 1) in vec3 vertexColor;
layout(location = 2) in vec3 vertexNormal;
layout(location = 3) in vec3 vertexTangent;
layout(location = 4) in vec2 vertexTexCoord;

layout(location = 0) out vec3 fragColor;
layout(location = 1) out vec2 fragTexCoord;

layout(set = 0, binding = 0) uniform UBO {
	mat4 view;
	mat4 projection;
	mat4 viewProjection;
} CameraData;

layout (set = 0, binding = 1) readonly buffer StorageBuffer {
	mat4 model[];
} ObjectData;

void main() {
	gl_Position = CameraData.viewProjection * ObjectData.model[gl_InstanceIndex] * vec4(vertexPosition, 1.0);
	fragColor = vec3(max(dot(vertexNormal, normalize(vec3(5,5,5))), 0));
	fragTexCoord = vertexTexCoord;
}
