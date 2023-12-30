import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms
from torch.autograd import Variable

def init_weights(m):
    if isinstance(m, nn.Linear):
        torch.nn.init.xavier_uniform_(m.weight)
        m.bias.data.fill_(0.01)

class TreeMortMixin:
    def post_init(self):
        self.apply(init_weights)

    def save(self, fname, nfeatures=None):
        torch.save(self.state_dict(), fname)


class Net(nn.Module, TreeMortMixin):
    def __init__(self, nfeatures):
        super(Net, self).__init__()
        self.nfeatures = nfeatures
        self.fc1  = nn.Linear(nfeatures, 128)
        self.fc2  = nn.Linear(128, 16)
        self.fc3 = nn.Linear(16, 16)
        self.fc4  = nn.Linear(16, 8)
        self.fc5  = nn.Linear(8, 8)
        self.fc6  = nn.Linear(8, 8)
        self.fc7  = nn.Linear(8, 1)
        
    def forward(self, x):
        x= F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        #x = F.dropout(x, 0.05)
        x = F.relu(self.fc3(x))
        x = F.relu(self.fc4(x))
        x = F.relu(self.fc5(x))
        x = F.relu(self.fc6(x))
        x = self.fc7(x)
        return torch.sigmoid(x)
    

class Net_10ReLU(nn.Module, TreeMortMixin):
    def __init__(self, nfeatures):
        super(Net_10ReLU, self).__init__()
        self.fc1  = nn.Linear(nfeatures, 128)
        self.fc2  = nn.Linear(128, 100)
        self.fc3  = nn.Linear(100, 64)
        self.fc4  = nn.Linear(64, 48)
        self.fc5  = nn.Linear(48, 32)
        self.fc6  = nn.Linear(32, 24)
        self.fc7  = nn.Linear(24, 16)
        self.fc8  = nn.Linear(16, 12)
        self.fc9  = nn.Linear(12, 8)
        self.fc10 = nn.Linear(8, 1)
        
    def forward(self, x):
        x= F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        #x = F.dropout(x, 0.05)
        x = F.relu(self.fc3(x))
        x = F.relu(self.fc4(x))
        x = F.relu(self.fc5(x))
        x = F.relu(self.fc6(x))
        x = F.relu(self.fc7(x))
        x = F.relu(self.fc8(x))
        x = F.relu(self.fc9(x))
        x = F.relu(self.fc10(x))
        return torch.sigmoid(x)

class OptiModel(nn.Module, TreeMortMixin):
    def __init__(self, nfeatures, output_bias=None):
        super(OptiModel, self).__init__()
        self.dense1 = nn.Linear(nfeatures, 24)
        self.dense2 = nn.Linear(24, 24)
        self.dense3 = nn.Linear(24, 24)
        self.dense4 = nn.Linear(24, 24)
        self.dense5 = nn.Linear(24, 24)
        self.dense6 = nn.Linear(24, 24)
        self.dense7 = nn.Linear(24, 24)
        self.dense8 = nn.Linear(24, 24)
        self.dropout = nn.Dropout(p=0.5)
        self.dense9 = nn.Linear(24, 1)
        self.output = nn.Sigmoid()
        if self.output_bias is not None:
            self.output.bias.data.fill_(output_bias)

    def forward(self, x):
        x = F.relu(self.dense1(x))
        x = F.relu(self.dense2(x))
        x = F.relu(self.dense3(x))
        x = F.relu(self.dense4(x))
        x = F.relu(self.dense5(x))
        x = F.relu(self.dense6(x))
        x = F.relu(self.dense7(x))
        x = F.relu(self.dense8(x))
        logits = self.output(self.dense9(x))
        return logits

class SigmoidNet(nn.Module, TreeMortMixin):
    def __init__(self, nfeatures):
        super(SigmoidNet, self).__init__()
        self.fc1  = nn.Linear(nfeatures, 64)
        self.fc2  = nn.Linear(64, 32)
        self.fc3  = nn.Linear(32, 24)
        self.fc4  = nn.Linear(24, 12)
        self.fc5  = nn.Linear(12, 8)
        self.fc6  = nn.Linear(8, 1)

        self.s1   = nn.Sigmoid()
        self.s2   = nn.Sigmoid()
        self.s3   = nn.Sigmoid()
        self.s4   = nn.Sigmoid()
        self.s5   = nn.Sigmoid()

        
    def forward(self, x):
        x= F.relu(self.fc1(x))
        x = self.s1(x)

        x = self.fc2(x)
        x = self.s2(x)

        x = self.fc3(x)
        x = self.s3(x)

        x = self.fc4(x)
        x = self.s4(x)

        x = self.fc5(x)
        x = self.s5(x)

        x = self.fc6(x)
        return torch.sigmoid(x)
