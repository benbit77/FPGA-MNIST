import torch
import torch.nn as nn
import torchvision

torch.manual_seed(0)

transform = torchvision.transforms.Compose([torchvision.transforms.ToTensor()])

train_data = torchvision.datasets.MNIST('./data', train=True, download=True, transform=transform)
test_data = torchvision.datasets.MNIST('./data', train=False, download=True, transform=transform)

train_loader = torch.utils.data.DataLoader(train_data, batch_size=64, shuffle=True)
test_loader = torch.utils.data.DataLoader(test_data, batch_size=1000)

model = nn.Sequential(
    nn.Flatten(),        # (1, 28, 28) -> (784,)
    nn.Linear(784, 64),  # y = Wx + b, W is 64x784
    nn.ReLU(),
    nn.Linear(64, 10),   # 10 outputs, one per digit
)

loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

for epoch in range(5):
    for batch, (images, labels) in enumerate(train_loader):
        optimizer.zero_grad()          # clear last batch's gradients
        outputs = model(images)        # forward pass
        loss = loss_fn(outputs, labels)
        loss.backward()                # compute gradients
        optimizer.step()               # update weights
        if batch % 200 == 0:
            print(f"epoch {epoch}, batch {batch}, loss {loss.item():.4f}")

model.eval()
correct = 0
with torch.no_grad():
    for images, labels in test_loader:
        predicted = model(images).argmax(dim=1)
        correct += (predicted == labels).sum().item()

print(f"Test accuracy: {100 * correct / len(test_data):.2f}%")
torch.save(model.state_dict(), 'py/model_float.pt')