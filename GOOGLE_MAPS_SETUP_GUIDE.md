# 🗺️ Google Maps Integration Setup Guide

## Step 1: Get Google Maps API Key

1. **Go to Google Cloud Console:**

   - Visit: https://console.cloud.google.com/
   - Sign in with your Google account

2. **Create or Select a Project:**

   - Create a new project or select an existing one
   - Project name example: "Tourism Indonesia Maps"

3. **Enable Required APIs:**

   - Go to "APIs & Services" → "Library"
   - Search and enable these APIs:
     - **Maps JavaScript API**
     - **Places API** (optional, for better place search)
     - **Maps Embed API**

4. **Create API Key:**

   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "API Key"
   - Copy your API key (it looks like: `AIzaSyC1234567890abcdef`)

5. **Secure Your API Key (Recommended):**
   - Click on your API key to edit it
   - Under "Application restrictions", select "HTTP referrers"
   - Add your domain (e.g., `localhost:*` for development)

## Step 2: Configure Your Environment

1. **Create .env file in tourism_frontend directory:**

   ```bash
   cd /home/hasbi/deploycamp/tourism_frontend
   cp .env.example .env
   ```

2. **Edit the .env file:**

   ```env
   # API Configuration
   API_BASE_URL=http://localhost:8000
   API_TIMEOUT=30

   # Google Maps Configuration
   GOOGLE_MAPS_API_KEY=your_actual_api_key_here

   # Development Settings
   DEBUG=False
   ```

   **Replace `your_actual_api_key_here` with your real Google Maps API key**

## Step 3: Install Dependencies

```bash
cd /home/hasbi/deploycamp
source venv/bin/activate
pip install python-dotenv
```

## Step 4: Test the Application

1. **Start the Streamlit app:**

   ```bash
   cd /home/hasbi/deploycamp
   source venv/bin/activate
   streamlit run tourism_frontend/app.py --server.port=8501
   ```

2. **Open your browser:**

   - Go to: http://localhost:8501

3. **Test Google Maps features:**

   - Go to the **🗺️ Maps** tab
   - Select a place from the dropdown
   - Look for these features:
     - **📍 View on Google Maps** button
     - **🧭 Get Directions** button
     - Embedded map (if API key is configured)
     - Coordinates display

4. **Test in Recommendations:**
   - Go to **🎯 Recommendations** tab
   - Set your preferences and get recommendations
   - Each place card should show:
     - Location & Maps section
     - Google Maps links
     - Coordinates (if available)

## Step 5: Verification Checklist

✅ **Maps Tab Works:**

- [ ] Maps tab appears in navigation
- [ ] Place selector dropdown works
- [ ] Map summary stats show correct info
- [ ] "View on Google Maps" links open in new tab
- [ ] "Get Directions" links work

✅ **Place Cards Have Maps:**

- [ ] Each place card shows "🗺️ Location & Maps" section
- [ ] Google Maps buttons work
- [ ] Coordinates are displayed (when available)

✅ **Embedded Maps (with API key):**

- [ ] Interactive embedded map shows in Maps tab
- [ ] Map shows correct location for selected place
- [ ] Map is properly sized and responsive

## Troubleshooting

### Issue: "Google Maps API key not configured"

**Solution:**

- Check your `.env` file has the correct `GOOGLE_MAPS_API_KEY=your_key`
- Restart the Streamlit app after adding the key
- Make sure there are no spaces around the equals sign

### Issue: Maps don't load or show errors

**Solution:**

- Verify your API key is correct
- Check that Maps JavaScript API and Maps Embed API are enabled
- Check browser console for error messages
- Ensure your API key isn't restricted to other domains

### Issue: "This page didn't load Google Maps correctly"

**Solution:**

- Your API key might be restricted
- Go to Google Cloud Console → Credentials → Edit your API key
- Under "Application restrictions", select "None" (for testing)
- Or add `localhost:*` to HTTP referrers

### Issue: Links open but show wrong location

**Solution:**

- Some places might not have coordinates in the system
- The app will fallback to searching by place name
- This is normal behavior for places without exact coordinates

## Testing Different Scenarios

### Test 1: Without API Key

1. Don't set `GOOGLE_MAPS_API_KEY` in `.env`
2. Maps tab should show "Not Configured" warning
3. Basic Google Maps links should still work
4. No embedded maps should appear

### Test 2: With API Key

1. Set valid `GOOGLE_MAPS_API_KEY` in `.env`
2. Restart the app
3. Maps tab should show embedded interactive maps
4. All features should work

### Test 3: Different Places

1. Try different places from the dropdown
2. Check if coordinates are shown
3. Verify maps point to correct locations
4. Test both "View on Google Maps" and "Get Directions"

## What You Should See

### Maps Tab Features:

- 📊 Statistics showing places with maps and cities covered
- 🗺️ Interactive place selector
- 📍 Embedded Google Map (with API key)
- 📋 Place details for selected location
- 💡 Usage tips

### Place Cards Features:

- 🗺️ "Location & Maps" section
- 📍 "View on Google Maps" button
- 🧭 "Get Directions" button
- 📍 Coordinates display (when available)

## Need Help?

If you encounter issues:

1. Check the browser console for JavaScript errors
2. Verify your API key in Google Cloud Console
3. Make sure all required APIs are enabled
4. Try restarting the Streamlit app after configuration changes

The app gracefully handles missing API keys - basic map links will work even without the API key configured!
