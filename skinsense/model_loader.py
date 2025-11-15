import os
import sys

# Lazy load the model to avoid startup errors
skin_model = None

def get_model():
    """Lazy load the skin disease model"""
    global skin_model
    
    if skin_model is not None:
        return skin_model
    
    try:
        from tensorflow.keras.models import load_model
        import tensorflow as tf
    except ImportError:
        raise ImportError(
            "TensorFlow is not installed. Please install it with:\n"
            "pip install tensorflow"
        )
    
    # Check for ResNet50 model first (new model)
    MODEL_PATH_RESNET = os.path.join(
        os.path.dirname(__file__),
        "model",
        "final_ResNet50_model.h5"
    )
    
    # Fallback to MobileNetV2 (old model)
    MODEL_PATH = os.path.join(
        os.path.dirname(__file__),
        "model",
        "final_MobileNetV2_model.keras"
    )
    
    MODEL_PATH_H5 = MODEL_PATH.replace('.keras', '.h5')
    loaded_model = None
    
    # Check for ResNet50 weights file
    WEIGHTS_PATH_RESNET = MODEL_PATH_RESNET.replace('.h5', '_weights.h5')
    
    # Try ResNet50 weights first (more reliable)
    if os.path.exists(WEIGHTS_PATH_RESNET):
        print(f"Loading ResNet50 weights from: {WEIGHTS_PATH_RESNET}")
        try:
            from tensorflow.keras.applications import ResNet50
            from tensorflow.keras.models import Sequential
            from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
            
            # Rebuild architecture EXACTLY as trained in Colab
            base_model = ResNet50(
                weights='imagenet',
                include_top=False,
                input_shape=(224, 224, 3)
            )
            base_model.trainable = False
            
            loaded_model = Sequential([
                base_model,
                GlobalAveragePooling2D(),
                Dense(256, activation='relu'),
                Dropout(0.5),
                Dense(6, activation='softmax')  # 6 classes
            ])
            
            # Load the trained weights
            loaded_model.load_weights(WEIGHTS_PATH_RESNET)
            
            print("✅ ResNet50 weights loaded successfully!")
            print(f"   Model has {len(loaded_model.layers)} layers")
        except Exception as e:
            print(f"Failed to load ResNet50 weights: {e}")
    
    # Try loading full ResNet50 model
    elif os.path.exists(MODEL_PATH_RESNET):
        print(f"Loading ResNet50 model from: {MODEL_PATH_RESNET}")
        try:
            # Try loading with compile=False to avoid optimizer issues
            loaded_model = load_model(MODEL_PATH_RESNET, compile=False)
            print("✅ ResNet50 model loaded successfully!")
            print(f"   Model has {len(loaded_model.layers)} layers")
            print(f"   Input shape: {loaded_model.input_shape}")
            print(f"   Output shape: {loaded_model.output_shape}")
        except Exception as e:
            error_msg = str(e)
            print(f"Failed to load ResNet50: {error_msg}")
            
            # If it's a layer connection issue, rebuild with Sequential API (matching Colab)
            if "received 2 input tensors" in error_msg or "Layer count mismatch" in error_msg:
                print("Rebuilding with Sequential API to match training architecture...")
                try:
                    from tensorflow.keras.applications import ResNet50
                    from tensorflow.keras.models import Sequential
                    from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
                    
                    # Rebuild EXACTLY as in Colab training code
                    base_model = ResNet50(
                        weights='imagenet',
                        include_top=False,
                        input_shape=(224, 224, 3)
                    )
                    base_model.trainable = False
                    
                    loaded_model = Sequential([
                        base_model,
                        GlobalAveragePooling2D(),
                        Dense(256, activation='relu'),
                        Dropout(0.5),
                        Dense(6, activation='softmax')
                    ])
                    
                    # Load weights from the saved file
                    loaded_model.load_weights(MODEL_PATH_RESNET)
                    print("✅ ResNet50 rebuilt with Sequential API and weights loaded!")
                except Exception as e2:
                    print(f"Failed to rebuild and load weights: {e2}")
    
    # Try loading .keras file first (your trained model)
    if os.path.exists(MODEL_PATH):
        print(f"Attempting to load .keras file: {MODEL_PATH}")
        try:
            # Try different loading methods for .keras file
            loaded_model = load_model(MODEL_PATH, compile=False, safe_mode=False)
            print(f"Successfully loaded .keras model!")
        except Exception as e:
            print(f"Failed to load .keras file: {e}")
            print(f"Trying .h5 fallback...")
    
    # Fallback to .h5 if .keras failed or doesn't exist
    if loaded_model is None and os.path.exists(MODEL_PATH_H5):
        print(f"Loading model from .h5 file: {MODEL_PATH_H5}")
        try:
            # Try direct load
            loaded_model = load_model(MODEL_PATH_H5, compile=False)
            print("✅ Direct load successful!")
        except Exception as e:
            error_msg = str(e)
            print(f"Direct load failed: {error_msg}")
            
            # If the error is about "received 2 input tensors", rebuild architecture
            if "received 2 input tensors" in error_msg:
                print("Attempting to rebuild model with Functional API...")
                try:
                    from tensorflow.keras.applications import MobileNetV2
                    from tensorflow.keras.models import Model
                    from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
                    
                    # Rebuild the Functional API model
                    base_model = MobileNetV2(
                        weights='imagenet',
                        include_top=False,
                        input_shape=(224, 224, 3)
                    )
                    base_model.trainable = False
                    
                    x = base_model.output
                    x = GlobalAveragePooling2D()(x)
                    x = Dropout(0.3)(x)
                    x = Dense(128, activation='relu')(x)
                    outputs = Dense(6, activation='softmax')(x)
                    
                    loaded_model = Model(inputs=base_model.input, outputs=outputs)
                    
                    # Load trained weights
                    loaded_model.load_weights(MODEL_PATH_H5)
                    print("✅ Model rebuilt and weights loaded successfully!")
                    
                except Exception as e2:
                    print(f"Weight loading failed: {e2}")
                    raise RuntimeError(f"Failed to load model: {str(e2)}")
            else:
                raise RuntimeError(f"Failed to load model: {error_msg}")
    
    if loaded_model is None:
        raise FileNotFoundError(
            f"Could not load model from {MODEL_PATH} or {MODEL_PATH_H5}\n"
            "Please run train_model.py to create a valid model file."
        )
    
    # Recompile the model
    try:
        loaded_model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        print(f"Model loaded successfully (TensorFlow {tf.__version__})")
        print(f"Input shape: {loaded_model.input_shape}")
        print(f"Output shape: {loaded_model.output_shape}")
        
        skin_model = loaded_model
        return skin_model
    except Exception as e:
        error_msg = str(e)
        print(f"Error loading model: {error_msg}")
        
        if "received 2 input tensors" in error_msg:
            print("\n=== MODEL FILE IS CORRUPTED ===")
            print("The model file has a structural error and needs to be retrained.")
            print("Please run train_model.py again to regenerate the model file.")
        
        raise RuntimeError(f"Failed to load model: {error_msg}")
