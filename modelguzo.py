import torch
from torchvision import models
from bing_image_downloader import downloader  # 크롤링용


model = models.resnet34(pretrained=True)
model = torch.load('sgd106.pth')
print(model)