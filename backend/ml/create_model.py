"""
AgriVision AI — Create Initial Model

Creates a MobileNetV2-based model with the exact architecture expected
by the application. Uses ImageNet pretrained weights for the base model
so feature extraction is real — only the classifier head is untrained.

This allows the full inference pipeline to work end-to-end immediately.
For production accuracy, train with: python ml/train.py --data-dir ./datasets/plantvillage

Usage:
    python ml/create_model.py
"""

import os
import sys

# Suppress TF warnings for clean output
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# Constants matching the app's config
IMAGE_SIZE = 224
NUM_CLASSES = 40  # 38 PlantVillage classes + 2 extras from class_mapping.json (indices 0-39)


def create_model() -> keras.Model:
    """
    Build the exact same MobileNetV2 architecture used in train.py
    but without data augmentation layers (inference-only model).
    """
    # Input
    inputs = keras.Input(shape=(IMAGE_SIZE, IMAGE_SIZE, 3))

    # MobileNetV2 base with ImageNet weights (real feature extraction)
    base_model = keras.applications.MobileNetV2(
        input_shape=(IMAGE_SIZE, IMAGE_SIZE, 3),
        include_top=False,
        weights="imagenet",
    )
    base_model.trainable = False

    x = base_model(inputs, training=False)

    # Classifier head (same architecture as train.py)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dropout(0.3)(x)
    x = layers.Dense(256, activation="relu")(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dropout(0.2)(x)
    outputs = layers.Dense(NUM_CLASSES, activation="softmax")(x)

    model = keras.Model(inputs, outputs, name="AgriVision_MobileNetV2")
    return model


def main():
    print("=" * 60)
    print("AgriVision AI — Creating Initial Model")
    print("=" * 60)

    # Create output directory
    output_dir = os.path.join(os.path.dirname(__file__), "models")
    os.makedirs(output_dir, exist_ok=True)

    # Build model
    print("\n[1/3] Building MobileNetV2 model architecture...")
    model = create_model()
    model.summary()

    # Save model
    model_path = os.path.join(output_dir, "crop_disease_model.h5")
    print(f"\n[2/3] Saving model to: {model_path}")
    model.save(model_path)

    # Verify the model loads correctly
    print("\n[3/3] Verifying model loads correctly...")
    loaded_model = keras.models.load_model(model_path, compile=False)
    
    # Test with a dummy image
    dummy_input = np.random.rand(1, IMAGE_SIZE, IMAGE_SIZE, 3).astype(np.float32)
    predictions = loaded_model.predict(dummy_input, verbose=0)
    
    print(f"\n✅ Model created successfully!")
    print(f"   - Architecture: MobileNetV2 + Custom Head")
    print(f"   - Input shape: (None, {IMAGE_SIZE}, {IMAGE_SIZE}, 3)")
    print(f"   - Output classes: {NUM_CLASSES}")
    print(f"   - File size: {os.path.getsize(model_path) / (1024*1024):.1f} MB")
    print(f"   - Test prediction shape: {predictions.shape}")
    print(f"   - Test prediction sum: {predictions.sum():.4f} (should be ~1.0)")
    print(f"\n   Model saved to: {model_path}")
    print(f"\n⚠️  Note: This model uses ImageNet features with an untrained")
    print(f"   classifier head. For accurate predictions, train with:")
    print(f"   python ml/train.py --data-dir ./datasets/plantvillage")
    print("=" * 60)


if __name__ == "__main__":
    main()
