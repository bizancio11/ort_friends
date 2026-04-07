import torch
import torch.nn as nn
import torch.optim as optim

# 1. Preparación de datos (Tensores)
# X: Entradas, y: Salidas deseadas
X = torch.tensor([[1.0], [2.0], [3.0], [4.0]], dtype=torch.float32)
y = torch.tensor([[2.0], [4.0], [6.0], [8.0]], dtype=torch.float32)

# 2. Definición del modelo usando nn.Module
class LinearModel(nn.Module):
    def __init__(self):
        super(LinearModel, self).__init__()
        self.linear = nn.Linear(1, 1) # 1 entrada, 1 salida

    def forward(self, x):
        return self.linear(x)

model = LinearModel()

# 3. Función de pérdida y Optimizador
criterion = nn.MSELoss() # Error cuadrático medio
optimizer = optim.SGD(model.parameters(), lr=0.01) # Descenso de gradiente estocástico

# 4. Bucle de entrenamiento
for epoch in range(100):
    # Paso hacia adelante (Forward pass)
    predictions = model(X)
    loss = criterion(predictions, y)

    # Paso hacia atrás (Backward pass) y optimización
    optimizer.zero_grad() # Limpiar gradientes previos
    loss.backward()      # Calcular gradientes
    optimizer.step()     # Actualizar pesos

    if (epoch+1) % 20 == 0:
        print(f'Epoch [{epoch+1}/100], Loss: {loss.item():.4f}')

# 5. Predicción
test_input = torch.tensor([[5.0]])
print(f'Predicción para 5: {model(test_input).item():.4f}')
