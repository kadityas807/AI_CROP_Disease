"""Train MobileNetV2 on the curated 38-class PlantVillage split."""

import os
import time
import copy
import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim import lr_scheduler
from torchvision import datasets, models, transforms

# Config
DATA_DIR = "./data/processed/PlantVillage_Official_Split"
MODEL_SAVE_PATH = "./models/vision_mobilenetv2.pth"
BATCH_SIZE = 32
NUM_EPOCHS = 30
LEARNING_RATE = 0.0001

def get_dataloaders():
    """Setup data transforms and PyTorch Dataloaders."""
    if not os.path.exists(DATA_DIR):
        raise FileNotFoundError(f"Dataset not found at {DATA_DIR}. Run 01_dataset_setup.py first.")

    # Data augmentation and normalization for training
    # Just normalization for validation
    data_transforms = {
        'train': transforms.Compose([
            transforms.RandomResizedCrop(224),
            transforms.RandomHorizontalFlip(),
            transforms.RandomRotation(15),
            transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ]),
        'val': transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ]),
    }

    image_datasets = {
        x: datasets.ImageFolder(os.path.join(DATA_DIR, x), data_transforms[x])
        for x in ['train', 'val']
    }
    if len(image_datasets['train'].classes) != 38:
        raise ValueError(
            "The training split must contain exactly the 38 official PlantVillage classes. "
            "Run training/01_dataset_setup.py to create the curated split."
        )
    if image_datasets['train'].classes != image_datasets['val'].classes:
        raise ValueError("Training and validation class mappings do not match.")
    
    dataloaders = {
        x: torch.utils.data.DataLoader(
            image_datasets[x],
            batch_size=BATCH_SIZE,
            shuffle=(x == 'train'),
            num_workers=4,
        )
        for x in ['train', 'val']
    }
    
    dataset_sizes = {x: len(image_datasets[x]) for x in ['train', 'val']}
    class_names = image_datasets['train'].classes
    
    return dataloaders, dataset_sizes, class_names

def train_model(model, criterion, optimizer, scheduler, dataloaders, dataset_sizes, device, num_epochs=10):
    """Main training loop with validation tracking."""
    since = time.time()

    best_model_wts = copy.deepcopy(model.state_dict())
    best_acc = 0.0

    for epoch in range(num_epochs):
        print(f'Epoch {epoch}/{num_epochs - 1}')
        print('-' * 10)

        for phase in ['train', 'val']:
            if phase == 'train':
                model.train()  # Set model to training mode
            else:
                model.eval()   # Set model to evaluate mode

            running_loss = 0.0
            running_corrects = 0

            # Iterate over data
            for inputs, labels in dataloaders[phase]:
                inputs = inputs.to(device)
                labels = labels.to(device)

                optimizer.zero_grad()

                # Forward pass
                with torch.set_grad_enabled(phase == 'train'):
                    outputs = model(inputs)
                    _, preds = torch.max(outputs, 1)
                    loss = criterion(outputs, labels)

                    # Backward + optimize only if in training phase
                    if phase == 'train':
                        loss.backward()
                        optimizer.step()

                running_loss += loss.item() * inputs.size(0)
                running_corrects += torch.sum(preds == labels.data)

            if phase == 'train':
                scheduler.step()

            epoch_loss = running_loss / dataset_sizes[phase]
            epoch_acc = running_corrects.double() / dataset_sizes[phase]

            print(f'{phase} Loss: {epoch_loss:.4f} Acc: {epoch_acc:.4f}')

            # Deep copy the model if it's the best one so far
            if phase == 'val' and epoch_acc > best_acc:
                best_acc = epoch_acc
                best_model_wts = copy.deepcopy(model.state_dict())

        print()

    time_elapsed = time.time() - since
    print(f'Training complete in {time_elapsed // 60:.0f}m {time_elapsed % 60:.0f}s')
    print(f'Best val Acc: {best_acc:4f}')

    # Load best model weights
    model.load_state_dict(best_model_wts)
    return model

def main():
    print("=== SIH1638 Vision Model Training Pipeline ===")
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    
    print("Loading data...")
    dataloaders, dataset_sizes, class_names = get_dataloaders()
    print(f"Classes ({len(class_names)}): {class_names}")
    
    # Initialize MobileNetV2 for Transfer Learning
    print("Initializing MobileNetV2...")
    model = models.mobilenet_v2(weights=models.MobileNet_V2_Weights.DEFAULT)
    
    # Freeze early layers (optional, but speeds up initial training)
    # for param in model.parameters():
    #     param.requires_grad = False
        
    # Replace classifier head for our specific number of classes
    num_ftrs = model.classifier[1].in_features
    model.classifier[1] = nn.Linear(num_ftrs, len(class_names))
    model = model.to(device)

    # Fine-tune all layers using the training partition.
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)
    
    # Decay LR by a factor of 0.1 every 4 epochs
    exp_lr_scheduler = lr_scheduler.StepLR(optimizer, step_size=4, gamma=0.1)

    print("Starting training...")
    model = train_model(model, criterion, optimizer, exp_lr_scheduler, dataloaders, dataset_sizes, device, num_epochs=NUM_EPOCHS)
    
    # Save Model
    os.makedirs(os.path.dirname(MODEL_SAVE_PATH), exist_ok=True)
    torch.save(model.state_dict(), MODEL_SAVE_PATH)
    print(f"Model saved successfully to {MODEL_SAVE_PATH}")
    
    # Save class names mapping
    with open(os.path.join(os.path.dirname(MODEL_SAVE_PATH), "vision_classes.txt"), "w") as f:
        for c in class_names:
            f.write(f"{c}\n")

if __name__ == "__main__":
    main()
