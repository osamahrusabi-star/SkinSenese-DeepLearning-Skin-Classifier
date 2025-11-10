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
    
    MODEL_PATH = os.path.join(
        os.path.dirname(__file__),
        "model",
        "final_MobileNetV2_model.keras"
    )
    
    MODEL_PATH_H5 = MODEL_PATH.replace('.keras', '.h5')
    loaded_model = None
    
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
            loaded_model = load_model(MODEL_PATH_H5, safe_mode=False, compile=False)
        except Exception as e:
            error_msg = str(e)
            print(f"Error loading .h5 model: {error_msg}")
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
