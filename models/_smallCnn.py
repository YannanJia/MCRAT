import torch
import torch.nn as nn
import torch.nn.functional as F

class Expression(nn.Module):
    def __init__(self, func):
        super(Expression, self).__init__()
        self.func = func
    
    def forward(self, input):
        return self.func(input)

class Model(nn.Module):
    def __init__(self, i_c=1, n_c=10, reg_feature_dim=128):
        super(Model, self).__init__()

        self.conv1 = nn.Conv2d(i_c, 32, 5, stride=1, padding=2, bias=True)
        self.pool1 = nn.MaxPool2d((2, 2), stride=(2, 2), padding=0)

        self.conv2 = nn.Conv2d(32, 64, 5, stride=1, padding=2, bias=True)
        self.pool2 = nn.MaxPool2d((2, 2), stride=(2, 2), padding=0)


        self.flatten = Expression(lambda tensor: tensor.view(tensor.shape[0], -1))
        self.fc1 = nn.Linear(7 * 7 * 64, 1024, bias=True)
        self.fc2 = nn.Linear(1024, n_c)
        
        self.reshape = torch.nn.Sequential(
            # nn.Linear(1024, 512, bias=False),
            # nn.BatchNorm1d(512),
            # nn.ReLU(inplace=True),
            # nn.Linear(512, reg_feature_dim, bias=True)
            nn.Linear(1024, reg_feature_dim, bias=True)
        )


    def forward(self, x_i, mcrat=0):

        x_o = self.conv1(x_i)
        x_o = torch.relu(x_o)
        x_o = self.pool1(x_o)

        x_o = self.conv2(x_o)
        x_o = torch.relu(x_o)
        x_o = self.pool2(x_o)

        x_o = self.flatten(x_o)

        x_o = torch.relu(self.fc1(x_o))
        
        if mcrat==1:
            #--
            outF = self.reshape(x_o)
            outF = F.normalize(outF)
            #--
            return self.fc2(x_o), outF
        else:
            return self.fc2(x_o)
            


def smallNet():
    return Model()


