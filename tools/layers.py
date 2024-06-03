import numpy as np

#TODO still need to change the implementation by adding bias and changing the convolve method to be correct
class Convolutional:
    def __init__(self, kernel_width=3, kernel_height=3, padding=0, stride=1):
        self.kernel_width = kernel_width
        self.kernel_height = kernel_height
        self.kernel = np.random.randn(self.kernel_width, self.kernel_height)

    def convolve(self, img, padding=0, stride=1):
        x_kern_shape = self.kernel_width 
        y_kern_shape = self.kernel_height 
        x_img_shape = img.shape[0] 
        y_img_shape = img.shape[1]

        x_output = int((x_img_shape + (2 * padding) - x_kern_shape)/ stride) + 1
        y_output = int((y_img_shape + (2 * padding) - y_kern_shape)/ stride) + 1
        
        if padding != 0:
            image_padded = np.zeros((img.shape[0] + padding*2, img.shape[1] + padding*2))
            image_padded[int(padding):int(-1 * padding), int(padding):int(-1 * padding)] = img
        else:
            image_padded = img

        convolutions = np.zeros((x_output, y_output))

        for y in range(0, y_img_shape, stride):
            if y > (y_img_shape - y_kern_shape):
                break
            if y % stride == 0:
                for x in range(0, x_img_shape, stride):
                    if x > (x_img_shape - x_kern_shape):
                        break
                    try:
                        if x % stride == 0:
                            convolutions[x // stride, y // stride] = np.sum(
                                self.kernel * image_padded[x: x + x_kern_shape, y: y + y_kern_shape]
                            )
                    except:
                        break
        return convolutions
       
    def forward(self, input):
        self.input = input
        self.conv = self.convolve(input)
        print(self.conv)
        self.max_pool = self.max_pooling(self.conv)
        self.output = self.max_pool
        return self.output
    
    #add the backward propagation
    def backward(self, dvalues):
        pass



#TODO implement the pooling layer logic
class Pooling:
    def __init__(self, pooling_width=2, pooling_height=2, padding=0, stride=1):
        self.pooling_width = pooling_width
        self.pooling_height = pooling_height

    def max_pooling(self, convolved_image, padding=0):
        output_height = int(convolved_image.shape[0] // self.pooling_height)
        output_width = int(convolved_image.shape[1] // self.pooling_width)

        pooling = np.zeros((output_height, output_width))

        pooling_result = np.zeros((output_height, output_width))
        for i in range(0, output_height * self.pooling_height, self.pooling_height):
            for j in range(0, output_width * self.pooling_width, self.pooling_width):
                patch = convolved_image[i:i+self.pooling_height, j:j+self.pooling_height]
                result = np.max(patch)
                pooling_result[i // self.pooling_height, j // self.pooling_width] = result
        pooling = pooling_result

        return pooling
    
    def forward(self):
        pass

    def backward(self):
        pass


class Dense_layer:
    def __init__(self, n_inputs, n_neurons):
        self.weights = 0.1 * np.random.randn(n_inputs, n_neurons)
        self.biases = np.zeros((1, n_neurons));
    
    def forward(self, inputs):
        self.inputs = inputs
        self.output = np.dot(inputs, self.weights) + self.biases
        
    def backward(self, dvalues):
        self.dweights = np.dot(self.inputs.T, dvalues)
        self.dbiases = np.sum(dvalues, axis=0, keepdims=True)
        self.dinputs = np.dot(dvalues, self.weights.T)

    