import torch
import torch.nn as nn
import torch.nn.functional as F

class MLP(nn.Module):
    def __init__(self,input_size=64,class_num = 2):
        super(MLP,self).__init__()
        
        self.fc1 = nn.Linear(input_size,1024)
        self.fc2 = nn.Linear(1024,512)
        self.fc3 = nn.Linear(512,class_num)
    
    def forward(self,x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x
    

