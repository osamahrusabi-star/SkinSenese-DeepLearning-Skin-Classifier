# Gemini API Configuration Guide

## Quick Setup

1. **Get your Gemini API Key:**
   - Visit: https://aistudio.google.com/apikey
   - Click "Create API key"
   - Copy the generated key

2. **Configure your .env file:**
   - Open the file: `.env` (in your project root directory)
   - Replace `your_api_key_here` with your actual API key
   - Example:
     ```
     GEMINI_API_KEY=AIzaSyC1234567890abcdefghijklmnopqrs
     ```

3. **Restart Django server:**
   - Stop the server (Ctrl+C)
   - Start it again: `python manage.py runserver`

## Testing

After configuration, test the API by:
1. Upload an image in the dashboard
2. You should receive AI-powered skin condition advice

## Troubleshooting

### Error: "API key is not configured"
- Make sure you saved the `.env` file
- Verify the API key doesn't contain quotes or extra spaces
- Restart the Django server

### Error: "API key invalid"
- Check if your API key is correct
- Make sure you copied the entire key
- Generate a new key if needed

### AI advice shows error message
- The app will still work and show predictions
- Only the AI advice feature will be disabled
- Fix the API key to enable AI advice

## Security Notes

- **Never commit `.env` to Git** - it's already in `.gitignore`
- Keep your API key private
- Don't share screenshots containing your API key
- If you accidentally expose your key, delete it and create a new one at https://aistudio.google.com/apikey
