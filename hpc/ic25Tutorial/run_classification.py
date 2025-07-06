#######################################
# The code was adapted from this PyTorch online tutorial: https://pytorch.org/hub/pytorch_vision_resnet/
# It uses the dog image provided in the tutorial from https://github.com/pytorch/hub/blob/master/images/dog.jpg
# Additionally, we use 10 images of 5 cats and 5 dogs form Cats Vs. Dogs dataset https://huggingface.co/datasets/microsoft/cats_vs_dogs.
# Cats Vs Dogs dataset is a subset of Assira dataset, which consists of images from Petfinder.com that were manually classified by people [Elson et al., 2007].
# [Elson et al., 2007] Jeremy Elson, John (JD) Douceur, Jon Howell, and Jared Saul. 2007. Asirra: A CAPTCHA that Exploits Interest-Aligned Manual Image Categorization. In Proceedings of 14th ACM Conference on Computer and Communications Security (CCS) (proceedings of 14th acm conference on computer and communications security (ccs) ed.). Association for Computing Machinery, Inc. https://www.microsoft.com/en-us/research/publication/asirra-a-captcha-that-exploits-interest-aligned-manual-image-categorization/
#######################################
import torch
from PIL import Image
from torchvision import transforms
import time
import os
import argparse

# Preparing parser
parser = argparse.ArgumentParser()
parser.add_argument("--model", type=str, default="resnet50")
parser.add_argument("--oneImage", action="store_true") 
parser.add_argument("--runCuda", action="store_true") 
parser.add_argument("--topk", type=int, default=2) 

args = parser.parse_args()

model = torch.hub.load('pytorch/vision:v0.10.0', args.model, pretrained=True)

model.eval()

k = args.topk

preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

def run(model, preprocess, filename):
    if "cat" in filename:
        gold = "cat"
    elif "dog" in filename:
        gold = "dog"
    else:
        gold = -1
    
    input_image = Image.open(filename)
    input_tensor = preprocess(input_image)
    input_batch = input_tensor.unsqueeze(0) # create a mini-batch as expected by the model

    # move the input and model to GPU for speed if available
    if args.runCuda:
        input_batch = input_batch.to('cuda')
        model.to('cuda')
    
    with torch.no_grad():
        output = model(input_batch)
    
    # The output has unnormalized scores. To get probabilities, you can run a softmax on it.
    probabilities = torch.nn.functional.softmax(output[0], dim=0)

    return {"prediction": probabilities, "gold": gold}

def decode(probabilities_dict, k):
    # Read the categories
    with open("imagenet_classes.txt", "r") as f:
        categories = [s.strip() for s in f.readlines()]
    # Show top categories per image
    top5_prob, top5_catid = torch.topk(probabilities_dict["prediction"], k)
    print(f"========== Golden Answer: {probabilities_dict["gold"]} ==========")
    print(f"========== Top {k} probabilities: ==========")
    for i in range(top5_prob.size(0)):
        print(categories[top5_catid[i]], top5_prob[i].item())
    print(f"============================================")

if args.oneImage:
    filename = "./dog.jpg"
    start = time.time()

    results = run(model, preprocess, filename)
    decode(results, k)

    end = time.time()
    print(f"Code runtime: {end - start} seconds")
else:
    start = time.time()

    for file in os.listdir('./images'):
        filename = f"./images/{file}"
        results = run(model, preprocess, filename)
        decode(results, k)
    
    end = time.time()
    print(f"Code runtime: {end - start} seconds")