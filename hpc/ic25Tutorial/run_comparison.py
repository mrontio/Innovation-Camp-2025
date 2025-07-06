import torch
import numpy as np
import random
import time

# Setting seeds
random.seed(42)
torch.manual_seed(42)
np.random.seed(42)

# Preparing/Sampling data
numpy_data = np.random.uniform(0, 1, 1000000000)
torch_data = torch.from_numpy(numpy_data)
torch_cuda_data = torch_data.to('cuda')

# Numpy
start = time.time()

output = np.mean(numpy_data)

end = time.time()

print("================ Numpy ======================")
print(f"Shape: {numpy_data.shape}")
print(f"Top 10 elements {numpy_data[:10]}")
print(output)
print(f"Code runtime: {end - start} seconds")
print()

# Torch
start = time.time()

output = torch.mean(torch_data)

end = time.time()

print("================ Torch ======================")
print(f"Shape: {torch_data.shape}")
print(f"Top 10 elements {torch_data[:10]}")
print(output)
print(output.item())
print(f"Code runtime: {end - start} seconds")
print()

# Torch with CUDA
start = time.time()

output = torch.mean(torch_cuda_data)

end = time.time()

print("================ Torch CUDA =================")
print(f"Shape: {torch_cuda_data.shape}")
print(f"Top 10 elements {torch_cuda_data[:10]}")
print(output)
print(output.item())
print(f"Code runtime: {end - start} seconds")