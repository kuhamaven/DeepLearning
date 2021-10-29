# -*- coding: utf-8 -*-
"""TP.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1LFbJ5Eii1tlbldLvOLDh3Z5HjzSoMcoT
"""

uploader = widgets.FileUpload()
uploader
img = PILImage.create(uploader.data[0])

from google.colab import drive
import os

drive.mount('/content/drive')

os.chdir('/content/drive/MyDrive/Cuarto Año/Segundo Cuatrimestre/Deep Learning/Proyecto/skin_cancer')
print(os.getcwd())

"""Desde aca empieza el tp posta

ResNet VS Inception -
PyTorch
"""

pip install torch

import torch
import torch.optim as optim
import torch.nn as nn
from torchvision import datasets, models, transforms

from tqdm import tqdm

device = 'cuda' if torch.cuda.is_available() else 'cpu'

transform = transforms.Compose(
    [transforms.ToTensor(),
     transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

batch_size = 32

trainset = datasets.CIFAR10(root='./data', train=True,
                                        download=True, transform=transform)
trainset = datasets.ImageFolder('train', transform=transform)
trainloader = torch.utils.data.DataLoader(trainset, batch_size=batch_size,
                                          shuffle=True, num_workers=2)

testset = datasets.CIFAR10(root='./data', train=False,
                                       download=True, transform=transform)
testset = datasets.ImageFolder('Test', transform=transform)
testloader = torch.utils.data.DataLoader(testset, batch_size=batch_size,
                                         shuffle=False, num_workers=2)

# classes = ('plane', 'car', 'bird', 'cat',
#            'deer', 'dog', 'frog', 'horse', 'ship', 'truck')

lr = 0.001
model = models.resnet50(pretrained = True)
num_ftrs = model.fc.in_features
model.fc = nn.Linear(num_ftrs, 10)
model.to(device)

loss_fn = nn.CrossEntropyLoss()

optimizer = optim.Adagrad(model.parameters(),lr = lr)

epochs = 2
losses = []

def make_train_step(model, loss_fn, optimizer):
    # Builds function that performs a step in the train loop
    def train_step(x, y):
        # Sets model to TRAIN mode
        model.train()
        # Makes predictions
        yhat = model(x)
        # Computes loss
        #print(y)
        #print("ACA TERMINO EL Y NORMAL")
        #print(yhat)
        #print(y.shape)
        #print(torch.nn.functional.one_hot(y, num_classes=10))
        #print(yhat.shape)
        #print(yhat)
        one_hot = torch.nn.functional.one_hot(y,num_classes=10)
        loss = torch.nn.functional.cross_entropy(yhat,torch.max(one_hot, 1)[1])
        # Computes gradients
        loss.backward()
        # Updates parameters and zeroes gradients
        optimizer.step()
        optimizer.zero_grad()
        # Returns the loss
        return loss.item()
    
    # Returns the function that will be called inside the train loop
    return train_step

# Creates the train_step function for our model, loss function and optimizer
train_step = make_train_step(model, loss_fn, optimizer)

#print(model.state_dict())

for epoch in range(epochs):
   for x_batch, y_batch in tqdm(trainloader):
        x_batch = x_batch.to(device)
        y_batch = y_batch.to(device)
        #print(x_batch.shape)
        #print(y_batch.shape)
        loss = train_step(x_batch, y_batch)
        losses.append(loss)

#print(model.state_dict())