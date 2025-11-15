from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as django_login, logout as django_logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .gemini_client import generate_ai_response
#----------------------------------------------------------------------
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from tensorflow.keras.preprocessing import image
import numpy as np
import os
from .model_loader import get_model
from .gemini_client import generate_ai_response  # ✅ to talk to Gemini


# === HOME PAGE ===
def index(request):
    return render(request, 'skinsense/index.html')


# === ABOUT PAGE ===
def about_page(request):
    return render(request, 'skinsense/about.html')


# === TEAM MEMBER PAGES ===
def rusabi_page(request):
    return render(request, 'skinsense/Rusabi.html')

def mohanad_page(request):
    return render(request, 'skinsense/Mohanad.html')

def majeed_page(request):
    return render(request, 'skinsense/Majeed.html')


# === LOGIN PAGE ===
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            django_login(request, user)
            messages.success(request, f"Welcome back, {username}!")
            return redirect('skinsense:dashboard_page')  # ✅ important: use namespace
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('skinsense:login')
    return render(request, 'skinsense/login.html')

# === REGISTER PAGE ===
def register_page(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        User = get_user_model()

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('skinsense:register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('skinsense:register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('skinsense:register')

        # Create new user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = full_name
        user.is_active = True
        user.save()

        messages.success(request, "Account created successfully! Please log in.")
        return redirect('skinsense:login')

    return render(request, 'skinsense/register.html')


# === DASHBOARD PAGE ===
@login_required(login_url='skinsense:login')
def dashboard_page(request):
    return render(request, 'skinsense/dashboard.html')


# === FOLLOW-UP PAGE ===
@login_required(login_url='skinsense:login')
def followup_page(request):
    return render(request, 'skinsense/followup.html')


# === LOGOUT ===
def logout_user(request):
    django_logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('skinsense:login')

def gemini_api(request):
    """Handles Gemini API requests from frontend."""
    if request.method == "POST":
        import json
        body = json.loads(request.body)
        user_input = body.get("prompt", "")

        if not user_input:
            return JsonResponse({"error": "No prompt provided."}, status=400)

        try:
            ai_response = generate_ai_response(user_input)
            return JsonResponse({"response": ai_response})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)


# === GEMINI AI API (NEW ENDPOINT) ===
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .gemini_client import generate_ai_response


@csrf_exempt  # disable CSRF just for testing
def ai_advice_api(request):
    """Handle POST requests to send text to Gemini and return AI advice."""
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            user_text = body.get("text", "").strip()

            if not user_text:
                return JsonResponse({"error": "No text provided."}, status=400)

            ai_response = generate_ai_response(user_text)
            return JsonResponse({"response": ai_response})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)



@csrf_exempt
def analyze_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        img_file = request.FILES['image']
        temp_path = os.path.join('media', img_file.name)
        os.makedirs('media', exist_ok=True)

        # Save the uploaded file
        with open(temp_path, 'wb+') as f:
            for chunk in img_file.chunks():
                f.write(chunk)

        # Preprocess image for ResNet50 (using correct ResNet50 preprocessing)
        from tensorflow.keras.applications.resnet50 import preprocess_input
        img = image.load_img(temp_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)  # ResNet50 preprocessing

        # Get the model (lazy loaded)
        skin_model = get_model()
        
        # Predict with your CNN
        preds = skin_model.predict(img_array)
        class_index = np.argmax(preds)
        confidence = float(np.max(preds))

        # Update these to your actual dataset classes
        class_labels = ['acne', 'eczema', 'fungal infections', 'melasma', 'rosacea', 'vitiligo']
        predicted_condition = class_labels[class_index]

        # Determine risk level based on condition and confidence
        if predicted_condition in ['melasma', 'vitiligo']:
            risk_level = 'High'
        elif predicted_condition in ['eczema', 'rosacea']:
            risk_level = 'Medium'
        else:
            risk_level = 'Low'

        # Get smart advice from Gemini
        try:
            gemini_prompt = f"The user uploaded a skin image. The CNN model predicted {predicted_condition} with {confidence:.2%} confidence. Risk Level: {risk_level}. Provide detailed, user-friendly advice about this condition."
            ai_advice = generate_ai_response(gemini_prompt)
        except ValueError as e:
            # API key not configured
            ai_advice = (
                f"AI advice is currently unavailable (API key not configured).\n\n"
                f"Basic information about {predicted_condition}:\n"
                f"Please consult a dermatologist for proper diagnosis and treatment.\n\n"
                f"Error: {str(e)}"
            )
        except Exception as e:
            # Other errors
            ai_advice = (
                f"Unable to get AI advice at this time.\n\n"
                f"For {predicted_condition}, please consult a dermatologist.\n\n"
                f"Error: {str(e)}"
            )

        # Save to database if user is logged in
        if request.user.is_authenticated:
            from .models import Case
            from django.core.files.base import ContentFile
            
            # Re-read the file from temp path to save to database
            with open(temp_path, 'rb') as f:
                saved_image = ContentFile(f.read())
            
            case = Case.objects.create(
                user=request.user,
                condition=predicted_condition,
                confidence=confidence,
                risk_level=risk_level,
                advice=ai_advice
            )
            case.image.save(img_file.name, saved_image, save=True)

        # Remove temp image
        os.remove(temp_path)

        return JsonResponse({
            "condition": predicted_condition,
            "confidence": confidence,  # Return as float (0-1)
            "risk_level": risk_level,
            "advice": ai_advice
        })

    return JsonResponse({'error': 'Invalid request'}, status=400)


# === FOLLOW-UP API ===
@csrf_exempt
@login_required(login_url='skinsense:login')
def upload_followup(request):
    """Upload follow-up image and link it to a case"""
    if request.method == 'POST' and request.FILES.get('image'):
        from .models import Case, FollowUp
        
        case_id = request.POST.get('case_id')
        
        # If no case_id provided, use the most recent case
        if not case_id:
            latest_case = Case.objects.filter(user=request.user).order_by('-created_at').first()
            if not latest_case:
                return JsonResponse({'error': 'No previous case found. Please analyze an image first.'}, status=400)
            case_id = latest_case.id
        
        try:
            case = Case.objects.get(id=case_id, user=request.user)
        except Case.DoesNotExist:
            return JsonResponse({'error': 'Case not found'}, status=404)
        
        img_file = request.FILES['image']
        temp_path = os.path.join('media', img_file.name)
        os.makedirs('media', exist_ok=True)

        # Save the uploaded file
        with open(temp_path, 'wb+') as f:
            for chunk in img_file.chunks():
                f.write(chunk)

        # Preprocess and predict (using ResNet50 preprocessing)
        from tensorflow.keras.applications.resnet50 import preprocess_input
        img = image.load_img(temp_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)  # ResNet50 preprocessing

        skin_model = get_model()
        preds = skin_model.predict(img_array)
        class_index = np.argmax(preds)
        confidence = float(np.max(preds))

        class_labels = ['acne', 'eczema', 'fungal infections', 'melasma', 'rosacea', 'vitiligo']
        predicted_condition = class_labels[class_index]

        if predicted_condition in ['melasma', 'vitiligo']:
            risk_level = 'High'
        elif predicted_condition in ['eczema', 'rosacea']:
            risk_level = 'Medium'
        else:
            risk_level = 'Low'

        # Get AI advice
        try:
            gemini_prompt = f"Follow-up analysis: Previous diagnosis was {case.condition}. Current scan shows {predicted_condition} with {confidence:.2%} confidence. Provide progress assessment and advice."
            ai_advice = generate_ai_response(gemini_prompt)
        except:
            ai_advice = f"Follow-up for {predicted_condition}. Please consult your dermatologist."

        # Save follow-up to database
        from django.core.files.base import ContentFile
        
        # Re-read the file from temp path to save to database
        with open(temp_path, 'rb') as f:
            saved_image = ContentFile(f.read())
        
        followup = FollowUp.objects.create(
            case=case,
            condition=predicted_condition,
            confidence=confidence,
            risk_level=risk_level,
            advice=ai_advice
        )
        followup.image.save(img_file.name, saved_image, save=True)

        # Remove temp image
        os.remove(temp_path)

        return JsonResponse({
            "condition": predicted_condition,
            "confidence": confidence,
            "risk_level": risk_level,
            "advice": ai_advice,
            "case_id": case.id
        })

    return JsonResponse({'error': 'Invalid request'}, status=400)


# === GET USER HISTORY ===
@login_required(login_url='skinsense:login')
def get_history(request):
    """Get user's case history with follow-ups"""
    from .models import Case
    
    cases = Case.objects.filter(user=request.user).order_by('-created_at')
    
    history = []
    for case in cases:
        followups = []
        for followup in case.followups.all().order_by('created_at'):
            followups.append({
                'id': followup.id,
                'image': followup.image.url if followup.image else None,
                'condition': followup.condition,
                'confidence': followup.confidence,
                'risk_level': followup.risk_level,
                'date': followup.created_at.strftime('%Y-%m-%d %H:%M')
            })
        
        history.append({
            'id': case.id,
            'image': case.image.url if case.image else None,
            'condition': case.condition,
            'confidence': case.confidence,
            'risk_level': case.risk_level,
            'advice': case.advice,
            'date': case.created_at.strftime('%Y-%m-%d %H:%M'),
            'followups': followups
        })
    
    return JsonResponse({'history': history})