import onnx

input_width = 640
input_height = 480
model_path = "./model"
model_name = 'yolov7-tiny'
ONNX_MODEL = f'{model_path}/{model_name}-{input_height}-{input_width}.onnx'
onnx_model = onnx.load(ONNX_MODEL)

graph = onnx_model.graph
node  = graph.node
value_info = graph.value_info
input = graph.input 
output = graph.output 

for i in range (len(value_info)):
    # After onnx modifier modifification, node 364 become the output of the network
    # Node after 364 will not use anymore, so delete in here
    if value_info[i].name == "369":
        start_value_idx = i
        output_shape = []
        delete_value = len(value_info) - start_value_idx
        for x in value_info[i].type.tensor_type.shape.dim:
            output_shape.append(x.dim_value)

for j in range(delete_value):
    del value_info[start_value_idx]

# for i in range(len(node)):
#     # print("___________________{}_______________".format(i))
#     # print(node[i])
#     if node[i].output == ['364']:
#         start_node_idx = i
#         delete_node = len(node) - start_node_idx
#         output_node = onnx.helper.make_node(
#             "output",
#             inputs=["364"],
#             outputs=["output"],
#         )
#         # node.insert(start_node_idx+1, output_node) 
# for j in range(delete_node-1):
#     # print("___________delete______________")
#     # print(node[start_node_idx+1])
#     node.remove(node[start_node_idx+1])
# node.insert(start_node_idx+1, output_node) 

onnx.save(onnx_model, ONNX_MODEL)
