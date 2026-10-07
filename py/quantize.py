import torch
import torch.nn as nn
import torchvision

transform = torchvision.transforms.Compose([torchvision.transforms.ToTensor()])
train_data = torchvision.datasets.MNIST('./data', train=True, download=True, transform=transform)
train_loader = torch.utils.data.DataLoader(train_data, batch_size=64, shuffle=True)
test_data = torchvision.datasets.MNIST('./data', train=False, download=True, transform=transform)
test_loader = torch.utils.data.DataLoader(test_data, batch_size=1)

state = torch.load('py/model_float.pt')
print(state.keys())

s_x = 127
max_act = 0.0

W1 = state['1.weight']
s_w1 = 127 / W1.abs().max()
q_w1 = torch.round(W1 * s_w1).clamp(-128, 127).to(torch.int8)
q_b1 = torch.round(state['1.bias'] * s_w1 * s_x).to(torch.int32)

W2 = state['3.weight']
s_w2 = 127 / W2.abs().max()
q_w2 = torch.round(W2 * s_w2).clamp(-128, 127).to(torch.int8)

with torch.no_grad():
    for images, labels in train_loader:
        x = images.reshape(-1, 784)
        h = torch.relu(x @W1.T + state['1.bias'])
        max_act = max(max_act, h.max().item())

s_act = 127 / max_act
q_b2 = torch.round(state['3.bias'] * s_w2 * s_act).to(torch.int32)

def infer(q_img):
    acc1 = (q_w1.int() @ q_img.int()) + q_b1
    h = torch.clamp(torch.round(acc1.float() * s_act / (s_w1 * s_x)), 0, 127).to(torch.int8)
    acc2 = (q_w2.int() @ h.int()) + q_b2
    return acc2.argmax().item()

correct = 0
for img, label in test_loader:
    q_img = torch.round(img.flatten() * 127).clamp(-128,127).to(torch.int8)
    if infer(q_img) == label.item():
        correct += 1

print(f"Quantized accuracy: {100 * correct / 10000:.2f}%")

torch.save({'q_W1': q_w1, 'q_b1': q_b1, 'q_W2': q_w2, 'q_b2': q_b2,
            's_w1': s_w1, 's_w2': s_w2, 's_x': s_x, 's_act': s_act}, 'py/quantized.pt')