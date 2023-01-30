import torch
import torch.nn as nn

class Network(nn.Module):
    def __init__(self):
        super().__init__()

        # Layers
        self.m1 = nn.Linear(986, 986)
        self.f1 = nn.LeakyReLU()
        self.m2 = nn.Linear(986, 4096)
        self.f2 = nn.LeakyReLU()
        self.m3 = nn.Linear(4096, 1024)
        self.f3 = nn.LeakyReLU()
        self.m4 = nn.Linear(1024, 709)
        self.f4 = nn.Softmax(dim=1)

    def forward(self, x):
        x = self.m1(x)
        x = self.f1(x)
        x = self.m2(x)
        x = self.f2(x)
        x = self.m3(x)
        x = self.f3(x)
        x = self.m4(x)
        x = self.f4(x)

        return x



model = Network()
model.load_state_dict(torch.load('Machine Learning/model_weights.pth'))
print(model())
