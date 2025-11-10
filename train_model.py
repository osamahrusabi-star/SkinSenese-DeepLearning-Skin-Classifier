import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.optimizers import Adam
import os

# Paths
base_dir = r"C:\Users\Osamah Mohammed\Desktop\dataset\final_skin_dataset"
train_dir = os.path.join(base_dir, "train")
val_dir = os.path.join(base_dir, "valid")
test_dir = os.path.join(base_dir, "test")

# Image preprocessing
datagen = ImageDataGenerator(rescale=1.0/255)
train_gen = datagen.flow_from_directory(train_dir, target_size=(224, 224), batch_size=32)
val_gen = datagen.flow_from_directory(val_dir, target_size=(224, 224), batch_size=32)

# ✅ Correct base model setup
base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

# ✅ Freeze base model layers
base_model.trainable = False

# ✅ Add classification layers properly
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dropout(0.3)(x)
x = Dense(128, activation='relu')(x)
outputs = Dense(train_gen.num_classes, activation='softmax')(x)

model = Model(inputs=base_model.input, outputs=outputs)

# Compile
model.compile(optimizer=Adam(learning_rate=0.0001),
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Train
model.fit(train_gen, validation_data=val_gen, epochs=5)

# ✅ Save the model in your Django project folder
save_path = r"C:\Users\Osamah Mohammed\Desktop\django\skinsense\model\final_MobileNetV2_model.keras"
model.save(save_path)
print(f"✅ Model saved successfully at: {save_path}")
