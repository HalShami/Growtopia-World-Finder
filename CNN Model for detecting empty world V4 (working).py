import tensorflow as tf
import matplotlib.pyplot as plt
import cv2
import os
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Define the data directories
train_data_dir = r"D:\Documents\PythonProjects\GT World Search\Project files\Data\testing"
validation_data_dir = r"D:\Documents\PythonProjects\GT World Search\Project files\Data\validation"
test_data_dir =  r"D:\Documents\PythonProjects\GT World Search\Project files\Data\testing"

# Data preprocessing and augmentation
train_datagen = ImageDataGenerator(rescale=1/242)
validation_datagen = ImageDataGenerator(rescale=1/242)
test_datagen = ImageDataGenerator(rescale=1/242)  # New test_datagen

# Create the train generator
train_generator = train_datagen.flow_from_directory(
    train_data_dir,
    target_size=(384, 216),  # Set the target size of the images
    batch_size=3,
    class_mode='binary'  # Use 'binary' for binary classification (2 classes)
)

# Create the validation generator
validation_generator = validation_datagen.flow_from_directory(
    validation_data_dir,
    target_size=(384, 216),  # Set the target size of the images
    batch_size=3,
    class_mode='binary'  # Use 'binary' for binary classification (2 classes)
)

# Create the model
model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(16, (3, 3), activation='relu', input_shape=(384, 216, 3)),
    tf.keras.layers.MaxPool2D(2, 2),
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu'),
    tf.keras.layers.MaxPool2D(2, 2),
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPool2D(2, 2),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

model.compile(loss='binary_crossentropy',
              optimizer=tf.keras.optimizers.RMSprop(learning_rate=0.001),  # Use 'learning_rate' instead of 'lr'
              metrics=['accuracy'])

# Train the model
history = model.fit(
    train_generator,
    steps_per_epoch=len(train_generator),
    epochs=20,
    validation_data=validation_generator,
    validation_steps=len(validation_generator)
)

# Evaluate the model on the test dataset
test_dataset = test_datagen.flow_from_directory(
    test_data_dir,
    target_size=(384, 216),
    batch_size=3,
    class_mode='binary'
)

test_loss, test_accuracy = model.evaluate(test_dataset)
print("Test Loss:", test_loss)
print("Test Accuracy:", test_accuracy)

model.save(r"D:\Documents\PythonProjects\GT World Search\Project files\Data\Saved Models\GT_World_DetectorV1.1.h5")