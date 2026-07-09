"""
AgriVision AI - Automated Model Training Pipeline

Downloads the PlantVillage dataset and trains the MobileNetV2 model.
Optimized for CPU training with limited RAM.

Usage:
    python ml/auto_train.py
"""

import os
import sys
import json
import shutil
import logging
from pathlib import Path

# Suppress TF info logs
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

# ============================================================
# CONFIG — optimized for CPU training with limited RAM
# ============================================================
IMAGE_SIZE = 160          # Smaller than 224 to save ~50% RAM
BATCH_SIZE = 8            # Small batch for CPU (prevents OOM)
EPOCHS_PHASE1 = 10        # Train classifier head (frozen base)
EPOCHS_PHASE2 = 5         # Fine-tune top layers
LEARNING_RATE = 1e-3
FINE_TUNE_LR = 1e-5
FINE_TUNE_LAYERS = 20    # Unfreeze last N layers of MobileNetV2
VALIDATION_SPLIT = 0.2
OUTPUT_DIR = Path("ml/models")
DATA_DIR = Path("datasets/plantvillage")
CLASS_MAPPING_PATH = Path("data/class_mapping.json")


def download_dataset():
    """Download PlantVillage dataset from Kaggle via kagglehub."""
    logger.info("=" * 60)
    logger.info("STEP 1: Downloading PlantVillage Dataset")
    logger.info("=" * 60)

    if DATA_DIR.exists() and any(DATA_DIR.iterdir()):
        # Check if it has class subdirectories
        subdirs = [d for d in DATA_DIR.iterdir() if d.is_dir()]
        if len(subdirs) >= 30:
            logger.info(f"Dataset already exists at {DATA_DIR} with {len(subdirs)} classes. Skipping download.")
            return str(DATA_DIR)

    try:
        import kagglehub
        logger.info("Downloading PlantVillage dataset from Kaggle...")
        logger.info("(This is ~3GB, may take 5-15 minutes depending on internet speed)")

        path = kagglehub.dataset_download("abdallahalidev/plantvillage-dataset")
        logger.info(f"Downloaded to: {path}")

        # Find the actual image directory (segmented or color)
        download_path = Path(path)
        # The dataset structure is: plantvillage-dataset/color/  or /segmented/ or /grayscale/
        # We want the 'color' variant
        candidates = [
            download_path / "plantvillage dataset" / "color",
            download_path / "plantvillage dataset" / "Color",
            download_path / "color",
            download_path / "Color",
            download_path,
        ]

        source_dir = None
        for candidate in candidates:
            if candidate.exists():
                subdirs = [d for d in candidate.iterdir() if d.is_dir()]
                if len(subdirs) >= 30:
                    source_dir = candidate
                    break

        if source_dir is None:
            # Search recursively for a directory with 30+ subdirectories
            for root, dirs, _ in os.walk(download_path):
                if len(dirs) >= 30:
                    source_dir = Path(root)
                    break

        if source_dir is None:
            logger.error(f"Could not find class directories in {download_path}")
            logger.info("Contents:")
            for item in download_path.rglob("*"):
                if item.is_dir():
                    logger.info(f"  DIR: {item.relative_to(download_path)}")
            raise RuntimeError("Dataset structure not recognized")

        # Create symlink or copy to expected location
        DATA_DIR.parent.mkdir(parents=True, exist_ok=True)
        if DATA_DIR.exists():
            shutil.rmtree(DATA_DIR)

        logger.info(f"Linking dataset from {source_dir} to {DATA_DIR}")
        # On Windows, use junction or copy
        try:
            # Try creating a junction (Windows equivalent of symlink for dirs)
            import subprocess
            subprocess.run(
                ["cmd", "/c", "mklink", "/J", str(DATA_DIR), str(source_dir)],
                check=True, capture_output=True
            )
        except Exception:
            logger.info("Junction failed, copying dataset (this may take a minute)...")
            shutil.copytree(str(source_dir), str(DATA_DIR))

        subdirs = [d for d in DATA_DIR.iterdir() if d.is_dir()]
        logger.info(f"Dataset ready: {len(subdirs)} classes found at {DATA_DIR}")
        return str(DATA_DIR)

    except ImportError:
        logger.error("kagglehub not installed. Run: pip install kagglehub")
        raise
    except Exception as e:
        logger.error(f"Download failed: {e}")
        logger.info("\nManual download instructions:")
        logger.info("1. Go to: https://www.kaggle.com/datasets/abdallahalidev/plantvillage-dataset")
        logger.info("2. Download and extract to: datasets/plantvillage/")
        logger.info("3. Ensure class folders are directly inside: datasets/plantvillage/<ClassName>/")
        raise


def train_model(data_dir: str):
    """Train the MobileNetV2 model on PlantVillage."""
    import numpy as np
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras import layers

    # Limit TF memory growth on CPU
    tf.config.threading.set_intra_op_parallelism_threads(2)
    tf.config.threading.set_inter_op_parallelism_threads(2)

    logger.info("=" * 60)
    logger.info("STEP 2: Training MobileNetV2 Model")
    logger.info("=" * 60)

    AUTOTUNE = tf.data.AUTOTUNE

    # --- Load dataset ---
    logger.info(f"Loading dataset from: {data_dir}")

    train_ds = keras.utils.image_dataset_from_directory(
        data_dir,
        validation_split=VALIDATION_SPLIT,
        subset="training",
        seed=42,
        image_size=(IMAGE_SIZE, IMAGE_SIZE),
        batch_size=BATCH_SIZE,
        label_mode="categorical",
    )

    val_ds = keras.utils.image_dataset_from_directory(
        data_dir,
        validation_split=VALIDATION_SPLIT,
        subset="validation",
        seed=42,
        image_size=(IMAGE_SIZE, IMAGE_SIZE),
        batch_size=BATCH_SIZE,
        label_mode="categorical",
    )

    class_names = train_ds.class_names
    num_classes = len(class_names)
    logger.info(f"Found {num_classes} classes")
    logger.info(f"Classes: {class_names[:5]}... (showing first 5)")

    # Performance optimization — NO .cache() to avoid OOM on CPU
    train_ds = train_ds.shuffle(500).prefetch(AUTOTUNE)
    val_ds = val_ds.prefetch(AUTOTUNE)

    # --- Build data augmentation (lightweight for CPU) ---
    data_augmentation = keras.Sequential([
        layers.RandomFlip("horizontal"),
        layers.RandomRotation(0.2),
    ], name="data_augmentation")

    # --- Build model ---
    logger.info("Building MobileNetV2 model...")

    inputs = keras.Input(shape=(IMAGE_SIZE, IMAGE_SIZE, 3))
    x = data_augmentation(inputs)
    x = layers.Rescaling(1.0 / 255)(x)

    base_model = keras.applications.MobileNetV2(
        input_shape=(IMAGE_SIZE, IMAGE_SIZE, 3),
        include_top=False,
        weights="imagenet",
    )
    base_model.trainable = False  # Freeze for Phase 1

    x = base_model(x, training=False)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dropout(0.3)(x)
    x = layers.Dense(256, activation="relu")(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dropout(0.2)(x)
    outputs = layers.Dense(num_classes, activation="softmax")(x)

    model = keras.Model(inputs, outputs, name="AgriVision_MobileNetV2")

    # --- Phase 1: Train classifier head ---
    logger.info("=" * 60)
    logger.info("PHASE 1: Training classifier head (base frozen)")
    logger.info(f"  Epochs: {EPOCHS_PHASE1}, LR: {LEARNING_RATE}")
    logger.info("=" * 60)

    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=LEARNING_RATE),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )

    callbacks_p1 = [
        keras.callbacks.EarlyStopping(
            monitor="val_accuracy", patience=5,
            restore_best_weights=True, verbose=1,
        ),
        keras.callbacks.ReduceLROnPlateau(
            monitor="val_loss", factor=0.5, patience=3,
            min_lr=1e-7, verbose=1,
        ),
    ]

    history1 = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=EPOCHS_PHASE1,
        callbacks=callbacks_p1,
    )

    p1_val_acc = max(history1.history["val_accuracy"])
    logger.info(f"Phase 1 best validation accuracy: {p1_val_acc:.4f}")

    # --- Phase 2: Fine-tune top layers ---
    logger.info("=" * 60)
    logger.info(f"PHASE 2: Fine-tuning last {FINE_TUNE_LAYERS} layers")
    logger.info(f"  Epochs: {EPOCHS_PHASE2}, LR: {FINE_TUNE_LR}")
    logger.info("=" * 60)

    base_model.trainable = True
    for layer in base_model.layers[:-FINE_TUNE_LAYERS]:
        layer.trainable = False

    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=FINE_TUNE_LR),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )

    callbacks_p2 = [
        keras.callbacks.EarlyStopping(
            monitor="val_accuracy", patience=5,
            restore_best_weights=True, verbose=1,
        ),
        keras.callbacks.ReduceLROnPlateau(
            monitor="val_loss", factor=0.5, patience=3,
            min_lr=1e-7, verbose=1,
        ),
        keras.callbacks.ModelCheckpoint(
            filepath=str(OUTPUT_DIR / "best_model.keras"),
            monitor="val_accuracy", save_best_only=True, verbose=1,
        ),
    ]

    history2 = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=EPOCHS_PHASE2,
        callbacks=callbacks_p2,
    )

    p2_val_acc = max(history2.history["val_accuracy"])
    best_val_acc = max(p1_val_acc, p2_val_acc)

    # --- Save model ---
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    model_path = OUTPUT_DIR / "crop_disease_model.h5"
    model.save(str(model_path))
    logger.info(f"Model saved to: {model_path}")

    # --- Save class mapping ---
    class_mapping = {}
    for i, name in enumerate(class_names):
        parts = name.split("___")
        crop = parts[0] if len(parts) > 1 else name.split("_")[0]
        disease = parts[1].replace("_", " ") if len(parts) > 1 else "Unknown"
        class_mapping[str(i)] = {
            "name": name,
            "crop": crop,
            "disease": disease if disease.lower() != "healthy" else "Healthy",
        }

    CLASS_MAPPING_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CLASS_MAPPING_PATH, "w") as f:
        json.dump(class_mapping, f, indent=4)
    logger.info(f"Class mapping saved to: {CLASS_MAPPING_PATH}")

    # --- Print results ---
    logger.info("=" * 60)
    logger.info("TRAINING COMPLETE!")
    logger.info(f"  Phase 1 best val accuracy: {p1_val_acc:.4f}")
    logger.info(f"  Phase 2 best val accuracy: {p2_val_acc:.4f}")
    logger.info(f"  Overall best val accuracy: {best_val_acc:.4f}")
    logger.info(f"  Total classes: {num_classes}")
    logger.info(f"  Model saved to: {model_path}")
    logger.info(f"  Model size: {model_path.stat().st_size / (1024*1024):.1f} MB")
    logger.info("=" * 60)

    return model, best_val_acc


def main():
    logger.info("=" * 60)
    logger.info("AgriVision AI - Automated Training Pipeline")
    logger.info("=" * 60)

    # Step 1: Download dataset
    data_dir = download_dataset()

    # Step 2: Train model
    model, accuracy = train_model(data_dir)

    if accuracy >= 0.95:
        logger.info("TARGET ACHIEVED: Model accuracy >= 95%%!")
    elif accuracy >= 0.90:
        logger.info("GOOD: Model accuracy >= 90%%. Consider more epochs for 95%%+.")
    else:
        logger.info("Model accuracy below target. Consider more data or training.")

    logger.info("Done! Restart the backend to load the new model.")


if __name__ == "__main__":
    main()
