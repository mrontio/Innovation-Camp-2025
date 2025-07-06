# Innovation Camp HPC Repository
The MINDS CDT + SustAI CDT Innovation Camp 2025 hackathon uses the Raspberry Pi and HPC to create an interesting demonstrator project for use in the British Science Festival and beyond!

This repository contains:
- Code to intialise a conda environment with PyTorch in it.
- Code to run the speed comparison between Numpy, PyTorch, and PyTorch with CUDA.
- Code to run the CNN example in the tutorial.
- A slurm file template that you can use when submitting your jobs to HPC.

We hope you enjoy this hackathon, and create something worth showing at the BSF and beyond!

## Directory Layout

- [ic25Tutorial/submitMe.slurm](./ic25Tutorial/submitMe.slurm): A slurm file template that you can utilise and adjust when submitting your jobs to HPC. It only includes some of the important #SBATCH settings.
- [ic25Tutorial/setup.sh](./ic25Tutorial/setup.sh): CONDA environment set-up used.
- [ic25Tutorial/run_comparison.py](./ic25Tutorial/run_comparison.py): Code used for comparing speed differences between Numpy, PyTorch, and PyTorch with CUDA.
- [ic25Tutorial/images/](./ic25Tutorial/images): 10 images of 5 cats and 5 dogs form Cats Vs. Dogs dataset https://huggingface.co/datasets/microsoft/cats_vs_dogs.
- [ic25Tutorial/run_classification.py](./ic25Tutorial/run_classification.py): Code used to run a CNN in the tutorial. The code was adapted from this PyTorch online tutorial: https://pytorch.org/hub/pytorch_vision_resnet/.
    - [ic25Tutorial/dog.jpg](./ic25Tutorial/dog.jpg): The code uses the dog image provided in the tutorial from https://github.com/pytorch/hub/blob/master/images/dog.jpg.
    - [ic25Tutorial/imagenet_classes.txt](./ic25Tutorial/imagenet_classes.txt): Imagenet class names. From https://pytorch.org/hub/pytorch_vision_resnet/.
