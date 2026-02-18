# Importar bibliotecas
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import torch
import torch.nn as nn
import torch.optim as optim

# ---------- 1️⃣ Gerar retina 3D simulada ----------
# Simulação simples de células ganglionares na retina
num_cells = 500
# posições x, y, z
x = np.random.uniform(-5, 5, num_cells)
y = np.random.uniform(-5, 5, num_cells)
z = np.random.uniform(-0.5, 0.5, num_cells)
# status: 1 = vivo, 0 = morto
status = np.random.choice([0,1], size=num_cells, p=[0.2,0.8])

# Visualização 3D
fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x[status==1], y[status==1], z[status==1], c='green', label='Vivo')
ax.scatter(x[status==0], y[status==0], z[status==0], c='red', label='Morto')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Retina 3D Simulada - Células Ganglionares')
ax.legend()
plt.show()

# ---------- 2️⃣ Preparar dados para IA ----------
X = np.vstack([x, y, z]).T
y_labels = status

# Converter para tensores do PyTorch
X_tensor = torch.tensor(X, dtype=torch.float32)
y_tensor = torch.tensor(y_labels, dtype=torch.float32).unsqueeze(1)

# ---------- 3️⃣ Criar IA simples (MLP) ----------
class SimpleNet(nn.Module):
    def __init__(self):
        super(SimpleNet, self).__init__()
        self.fc1 = nn.Linear(3, 16)
        self.fc2 = nn.Linear(16, 16)
        self.fc3 = nn.Linear(16, 1)
        self.sigmoid = nn.Sigmoid()
        
    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return self.sigmoid(x)

model = SimpleNet()
criterion = nn.BCELoss()
optimizer = optim.Adam(model.parameters(), lr=0.01)

# ---------- 4️⃣ Treinar IA ----------
epochs = 200
for epoch in range(epochs):
    optimizer.zero_grad()
    outputs = model(X_tensor)
    loss = criterion(outputs, y_tensor)
    loss.backward()
    optimizer.step()
    
    if (epoch+1) % 50 == 0:
        print(f"Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.4f}")

# ---------- 5️⃣ Testar IA ----------
with torch.no_grad():
    predicted = model(X_tensor).round()
accuracy = (predicted.eq(y_tensor).sum().item()) / num_cells
print(f"Accuracy na retina simulada: {accuracy*100:.2f}%")
