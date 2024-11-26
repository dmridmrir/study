import os
from PIL import Image
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms  
import matplotlib.pyplot as plt

# 데이터셋 정의
class CustomMultiClassDataset(Dataset):
    def __init__(self):
        self.base_dir = r''
        self.transform = transforms.Compose([
            transforms.Resize((128, 128)),
            transforms.ToTensor()
        ])
        self.image_pairs, self.labels = self.load_image_pairs()

    def load_images_from_folder(self, folder):
        images = []
        for root, _, files in os.walk(folder):
            for file in files:
                if file.endswith('.PNG'):
                    images.append(os.path.join(root, file))
        return images

    def load_image_pairs(self):
        image_pairs = []
        labels = []

        slide1_path = os.path.join(self.base_dir, '슬라이드1.PNG')
        slide2_path = os.path.join(self.base_dir, '슬라이드2.PNG')
        slide3_path = os.path.join(self.base_dir, '슬라이드3.PNG')

        # 슬라이드1 쌍 생성 및 라벨링
        equal8_images = self.load_images_from_folder(os.path.join(self.base_dir, 'equal', '8'))
        big8_images = self.load_images_from_folder(os.path.join(self.base_dir, 'big', '8'))
        small8_images = self.load_images_from_folder(os.path.join(self.base_dir, 'small', '8'))

        slide1_pairs = [(slide1_path, img) for img in equal8_images]
        slide1_pairs += [(slide1_path, img) for img in big8_images]
        slide1_pairs += [(slide1_path, img) for img in small8_images]
        slide1_labels = [0] * len(equal8_images) + [1] * len(big8_images) + [2] * len(small8_images)

        # 슬라이드2 쌍 생성 및 라벨링
        equal0_images = self.load_images_from_folder(os.path.join(self.base_dir, 'equal', '0'))
        big0_images = self.load_images_from_folder(os.path.join(self.base_dir, 'big', '0'))
        small0_images = self.load_images_from_folder(os.path.join(self.base_dir, 'small', '0'))

        slide2_pairs = [(slide2_path, img) for img in equal0_images]
        slide2_pairs += [(slide2_path, img) for img in big0_images]
        slide2_pairs += [(slide2_path, img) for img in small0_images]
        slide2_labels = [0] * len(equal0_images) + [1] * len(big0_images) + [2] * len(small0_images)

        # 슬라이드3 쌍 생성 및 라벨링
        equal4_images = self.load_images_from_folder(os.path.join(self.base_dir, 'equal', '4'))
        big4_images = self.load_images_from_folder(os.path.join(self.base_dir, 'big', '4'))
        small8_images_slide3 = self.load_images_from_folder(os.path.join(self.base_dir, 'small', '8'))

        slide3_pairs = [(slide3_path, img) for img in equal4_images]
        slide3_pairs += [(slide3_path, img) for img in big4_images]
        slide3_pairs += [(slide3_path, img) for img in small8_images_slide3]
        slide3_labels = [0] * len(equal4_images) + [1] * len(big4_images) + [2] * len(small8_images_slide3)

        image_pairs.extend(slide1_pairs + slide2_pairs + slide3_pairs)
        labels.extend(slide1_labels + slide2_labels + slide3_labels)

        return image_pairs, labels

    def __getitem__(self, index):
        img1_path, img2_path = self.image_pairs[index]
        
        # 두 이미지 로드 및 변환
        img1 = Image.open(img1_path).convert('L')
        img2 = Image.open(img2_path).convert('L')
        
        img1 = self.transform(img1)
        img2 = self.transform(img2)

        # 두 이미지를 채널 방향으로 결합
        combined_image = torch.cat((img1, img2), dim=0)  # (2, 128, 128)

        label = torch.tensor(self.labels[index], dtype=torch.long)
        return combined_image, label

    def __len__(self):
        return len(self.image_pairs)

# CNN 네트워크 정의 (다중 클래스 분류 모델)
class MultiClassCNN(nn.Module):
    def __init__(self):
        super(MultiClassCNN, self).__init__()
        self.conv1 = nn.Conv2d(2, 64, kernel_size=10)  
        self.conv2 = nn.Conv2d(64, 128, kernel_size=7)
        self.conv3 = nn.Conv2d(128, 128, kernel_size=4)
        self.conv4 = nn.Conv2d(128, 256, kernel_size=4)
        self.adaptive_pool = nn.AdaptiveAvgPool2d((6, 6))
        self.fc1 = nn.Linear(256 * 6 * 6, 4096)
        self.fc2 = nn.Linear(4096, 3)  # 3개 클래스 출력
    
    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.max_pool2d(x, 2)
        x = F.relu(self.conv2(x))
        x = F.max_pool2d(x, 2)
        x = F.relu(self.conv3(x))
        x = F.max_pool2d(x, 2)
        x = F.relu(self.conv4(x))
        x = self.adaptive_pool(x)
        x = x.view(x.size()[0], -1)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x

# 정확도 계산 함수
def compute_accuracy(output, labels):
    predicted = torch.argmax(output, dim=1)
    correct = (predicted == labels).float().sum()
    return correct / labels.size(0)

# 데이터 로드
dataset = CustomMultiClassDataset()
print(f"총 데이터셋 크기: {len(dataset)} 쌍")

# 훈련 및 검증 데이터 분할
train_size = int(0.8 * len(dataset))
val_size = len(dataset) - train_size
train_dataset, val_dataset = torch.utils.data.random_split(dataset, [train_size, val_size])

train_loader = DataLoader(train_dataset, shuffle=True, batch_size=32)
val_loader = DataLoader(val_dataset, shuffle=False, batch_size=32)

# 모델 및 옵티마이저 설정
model = MultiClassCNN()
criterion = nn.CrossEntropyLoss()  # 다중 클래스 손실 함수
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 학습 루프
num_epochs = 50
train_accuracies = []
val_accuracies = []
train_losses = []
val_losses = []

for epoch in range(num_epochs):
    # 훈련 단계
    model.train()
    total_train_loss = 0
    total_train_accuracy = 0
    for combined_image, label in train_loader:
        output = model(combined_image)  # 수정된 입력
        loss = criterion(output, label)
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        accuracy = compute_accuracy(output, label)
        total_train_loss += loss.item()
        total_train_accuracy += accuracy.item()

    avg_train_loss = total_train_loss / len(train_loader)
    avg_train_accuracy = total_train_accuracy / len(train_loader)
    train_losses.append(avg_train_loss)
    train_accuracies.append(avg_train_accuracy)
    
    # 검증 단계
    model.eval()
    total_val_loss = 0
    total_val_accuracy = 0
    with torch.no_grad():
        for combined_image, label in val_loader:
            output = model(combined_image)
            loss = criterion(output, label)
            
            accuracy = compute_accuracy(output, label)
            total_val_loss += loss.item()
            total_val_accuracy += accuracy.item()

    avg_val_loss = total_val_loss / len(val_loader)
    avg_val_accuracy = total_val_accuracy / len(val_loader)
    val_losses.append(avg_val_loss)
    val_accuracies.append(avg_val_accuracy)
    
    print(f'Epoch {epoch+1}/{num_epochs}, Training Loss: {avg_train_loss:.4f}, Training Accuracy: {avg_train_accuracy:.4f}, Validation Loss: {avg_val_loss:.4f}, Validation Accuracy: {avg_val_accuracy:.4f}')

# 그래프 그리기
# 정확도 그래프
plt.figure(figsize=(10, 5))
plt.plot(range(1, num_epochs + 1), train_accuracies, label='Training Accuracy')
plt.plot(range(1, num_epochs + 1), val_accuracies, label='Validation Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.title('Training and Validation Accuracy per Epoch')
plt.legend()
plt.grid(True)
plt.show()

# 손실 그래프
plt.figure(figsize=(10, 5))
plt.plot(range(1, num_epochs + 1), train_losses, label='Training Loss')
plt.plot(range(1, num_epochs + 1), val_losses, label='Validation Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.title('Training and Validation Loss per Epoch')
plt.legend()
plt.grid(True)
plt.show()

# 테스트 이미지 로드 함수
def load_test_image_pair(img1_path, img2_path, transform):
    img1 = Image.open(img1_path).convert('L')
    img2 = Image.open(img2_path).convert('L')
    img1 = transform(img1)
    img2 = transform(img2)
    combined_image = torch.cat((img1, img2), dim=0)
    return combined_image.unsqueeze(0)  # 배치 차원 추가

# 테스트 이미지 경로 설정
test_folder = r''
test_images = {
    "test_std": os.path.join(test_folder, 'test_std.PNG'),
    "test_s": os.path.join(test_folder, 'test_s.PNG'),
    "test_b": os.path.join(test_folder, 'test_b.PNG'),
    "test_e": os.path.join(test_folder, 'test_e.PNG'),
    "test2_std": os.path.join(test_folder, 'test2_std.PNG'),
    "test2_s": os.path.join(test_folder, 'test2_s.PNG'),
    "test2_b": os.path.join(test_folder, 'test2_b.PNG'),
    "test2_e": os.path.join(test_folder, 'test2_e.PNG'),
    "test3_std": os.path.join(test_folder, 'test3_std.PNG'),
    "test3_s": os.path.join(test_folder, 'test3_s.PNG'),
    "test3_b": os.path.join(test_folder, 'test3_b.PNG'),
    "test3_e": os.path.join(test_folder, 'test3_e.PNG')
}

# 테스트 쌍 생성
test_cases = [
    ("test_std", "test_s"),         #2
    ("test_std", "test_b"),         #1
    ("test_std", "test_e"),         #0
    ("test2_std", "test2_s"),       #2
    ("test2_std", "test2_b"),       #1
    ("test2_std", "test2_e"),       #0
    ("test3_std", "test3_s"),       #2
    ("test3_std", "test3_b"),       #1
    ("test3_std", "test3_e"),       #0
]

# 테스트 이미지 쌍 예측
model.eval()
with torch.no_grad():
    for std, compare in test_cases:
        img1_path = test_images[std]
        img2_path = test_images[compare]
        
        test_pair = load_test_image_pair(img1_path, img2_path, dataset.transform)
        output = model(test_pair)
        predicted_class = torch.argmax(output, dim=1).item()
        
        print(f"{std}와 {compare}의 예측 레이블: {predicted_class}")
