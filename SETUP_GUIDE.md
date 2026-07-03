# Wedding Invitation Website - Complete Setup Guide

This guide will help you set up the fully functional wedding invitation website with Google Sheets integration, background music, and scroll animations.

## Features

✅ **Mobile-First Responsive Design** - Works perfectly on all screen sizes
✅ **Google Sheets Integration** - RSVP responses saved automatically
✅ **Background Music** - Auto-plays on scroll (respects browser policies)
✅ **Scroll Reveal Animations** - Beautiful entrance effects
✅ **Live Countdown Timer** - Updates every second
✅ **Interactive Calendar** - Highlights wedding date
✅ **Google Maps Integration** - Direct link to venue

---

## Part 1: Google Sheets Setup (15 minutes)

### Step 1: Create Google Spreadsheet

1. Go to [Google Sheets](https://sheets.google.com)
2. Click **+ Blank** to create a new spreadsheet
3. Rename it to "Kyz Uzatuu RSVP Responses" or any name you prefer

### Step 2: Open Apps Script Editor

1. In your spreadsheet, click **Extensions** → **Apps Script**
2. A new tab will open with the Apps Script editor
3. Delete any existing code in the editor

### Step 3: Add the Script

1. Open the file `google-apps-script.js` from this project
2. Copy ALL the code
3. Paste it into the Apps Script editor
4. Click the **disk icon** (💾) or press `Ctrl+S` / `Cmd+S` to save
5. Name your project (e.g., "Wedding RSVP Backend")

### Step 4: Deploy as Web App

1. Click **Deploy** → **New deployment** (top right)
2. Click the ⚙️ icon next to "Select type"
3. Choose **Web app**
4. Fill in the settings:
   - **Description**: "Wedding RSVP Form Handler"
   - **Execute as**: **Me** (your Google account)
   - **Who has access**: **Anyone** (important!)
5. Click **Deploy**
6. Review permissions:
   - Click **Authorize access**
   - Select your Google account
   - Click **Advanced** → **Go to [Project Name] (unsafe)** (it's safe, don't worry)
   - Click **Allow**
7. **COPY THE WEB APP URL** - You'll need this in the next step!

### Step 5: Update Website Configuration

1. Open `index.html` in a text editor
2. Find this line (around line 1042):
   ```javascript
   const GOOGLE_SCRIPT_URL = 'YOUR_GOOGLE_SCRIPT_URL_HERE';
   ```
3. Replace `YOUR_GOOGLE_SCRIPT_URL_HERE` with the URL you copied
4. Save the file

**Example:**
```javascript
const GOOGLE_SCRIPT_URL = 'https://script.google.com/macros/s/AKfycbx.../exec';
```

---

## Part 2: Music Setup (5 minutes)

### Option A: Use Default Music (Quick)

The website comes with a default music URL. It will work but might not be ideal for a wedding.

### Option B: Add Your Own Music (Recommended)

1. **Find Your Music**:
   - Traditional Kyrgyz wedding music (recommended)
   - Or any instrumental music you prefer

2. **Upload Options**:

   **Option 1 - Google Drive** (easiest):
   - Upload your MP3 file to Google Drive
   - Right-click → **Get link** → Set to "Anyone with the link"
   - Copy the file ID from the URL
   - Format: `https://drive.google.com/uc?export=download&id=FILE_ID`

   **Option 2 - GitHub** (free hosting):
   - Create a GitHub repository
   - Upload the music file
   - Get the raw file URL

   **Option 3 - Your own hosting**:
   - Upload to your web server
   - Use the direct URL

3. **Update the HTML**:

   Open `index.html` and find (around line 860):
   ```html
   <source src="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3" type="audio/mpeg">
   ```

   Replace with your music URL:
   ```html
   <source src="YOUR_MUSIC_URL_HERE" type="audio/mpeg">
   ```

---

## Part 3: Customization (10 minutes)

### Update Wedding Details

Open `index.html` and customize:

1. **Bride's Name** (line 891):
   ```html
   <h1 class="hero-title">Алия</h1>
   ```

2. **Wedding Date** (line 893):
   ```html
   <div class="hero-date">08 · 08 · 2026</div>
   ```

3. **Hosts Names** (line 979):
   ```html
   <p>Карим <span class="ampersand">&amp;</span> Айым</p>
   ```

4. **Venue Location** (lines 935-936):
   ```html
   <p class="address-city reveal slide-left">Ош облусу, Ноокат шаары</p>
   <p class="address-venue reveal slide-right">«Ак Бермет» рестораны</p>
   ```

5. **Google Maps Link** (line 938):
   ```html
   <a href="https://maps.google.com/?q=Ак+Бермет+Ноокат" ...>
   ```
   Change the `q=` parameter to your venue name and location

6. **Countdown Timer** (line 1125):
   ```javascript
   const target = new Date(2026, 7, 8, 17, 0, 0).getTime();
   ```
   Format: `new Date(YEAR, MONTH-1, DAY, HOUR, MINUTE, SECOND)`
   Note: Month is 0-indexed (7 = August)

### Change Hero Image

1. Replace `images/hero-shokulo.png` with your photo
2. Keep the same filename, or update line 878:
   ```html
   <img src="images/YOUR_IMAGE.png" alt="" class="hero-bg">
   ```

---

## Part 4: Testing (5 minutes)

### Test Locally

1. Open `index.html` in your web browser
2. Test the RSVP form:
   - Enter a name
   - Select an attendance option
   - Click "Жөнөтүү" (Submit)
   - You should see the thank you message
3. Check your Google Spreadsheet - a new row should appear!

### Test Animations

1. Scroll down the page
2. Elements should smoothly fade/slide into view
3. Music should auto-play after scrolling (may require user interaction on some browsers)

---

## Part 5: Deployment (10 minutes)

### Option A: GitHub Pages (Free & Easy)

1. **Create GitHub Repository**:
   - Go to [GitHub](https://github.com)
   - Click **New repository**
   - Name it: `wedding-invitation`
   - Make it **Public**
   - Click **Create repository**

2. **Upload Files**:
   ```bash
   cd /path/to/kyz-uzatuu
   git init
   git add index.html images/
   git commit -m "Initial wedding invitation"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/wedding-invitation.git
   git push -u origin main
   ```

3. **Enable GitHub Pages**:
   - Go to repository **Settings**
   - Click **Pages** (left sidebar)
   - Source: **Deploy from a branch**
   - Branch: **main** → **/ (root)** → **Save**
   - Wait 1-2 minutes
   - Your site will be live at: `https://YOUR_USERNAME.github.io/wedding-invitation/`

### Option B: Netlify (Also Free)

1. Go to [Netlify](https://www.netlify.com)
2. Sign up / Log in
3. Drag and drop your `kyz-uzatuu` folder
4. Site will be live instantly!
5. You can customize the domain name

### Option C: Your Own Hosting

Upload via FTP/cPanel:
- `index.html`
- `images/` folder
- Any music files

---

## Part 6: Viewing RSVP Responses

### In Google Sheets

1. Open your Google Spreadsheet
2. You'll see a sheet named "RSVP Responses" with columns:
   - **Timestamp** - When submitted
   - **Name / Аты-жөнү** - Guest name(s)
   - **Response / Жооп** - Attendance status in Kyrgyz
   - **Response Code** - yes/both/no
   - **User Agent** - Browser info (for troubleshooting)

### Get Statistics

1. Open Apps Script editor
2. Select the function: **getRSVPStatistics**
3. Click **Run** (▶️)
4. View logs: **Execution log** (bottom)
5. You'll see:
   - Total responses
   - Number coming alone
   - Number coming with spouse
   - Cannot attend
   - **Estimated total guests**

---

## Troubleshooting

### Music Doesn't Auto-Play

**Cause**: Browser auto-play policies require user interaction
**Solution**: Visitors can click the music button in the top-right corner

### RSVP Not Saving to Sheets

1. Check the Google Script URL is correct in `index.html`
2. Ensure deployment is set to "Anyone" access
3. Check browser console for errors (F12 → Console tab)
4. Re-deploy the Apps Script if needed

### Scroll Animations Not Working

- Ensure JavaScript is enabled
- Try a different browser
- Check browser console for errors

### Mobile Display Issues

- The site is already mobile-optimized
- Clear browser cache
- Test in mobile view (F12 → Toggle device toolbar)

---

## Advanced Customization

### Change Color Scheme

All colors are in the CSS. Main colors:
- Background: `#FAF9F7`
- Text: `#4C463F`
- Accent: `#9A928B`

Search and replace these values in `index.html`

### Add More Animations

Add the `reveal` class with animation type:
- `reveal fade-in` - Fade in
- `reveal slide-up` - Slide from bottom
- `reveal slide-left` - Slide from left
- `reveal slide-right` - Slide from right
- `reveal scale-in` - Scale up

### Email Notifications

Uncomment the `sendEmailNotification` function in `google-apps-script.js` and add your email.

---

## Support Files

- `index.html` - Main website file
- `images/hero-shokulo.png` - Hero background image
- `google-apps-script.js` - Google Sheets backend code
- `README.md` - Project documentation
- `SETUP_GUIDE.md` - This file

---

## Need Help?

If you encounter issues:
1. Check the browser console for errors (F12)
2. Verify all URLs are correct
3. Ensure Google Apps Script is deployed with "Anyone" access
4. Test in incognito mode to rule out cache issues

---

## Quick Start Checklist

- [ ] Create Google Spreadsheet
- [ ] Deploy Apps Script
- [ ] Copy Web App URL
- [ ] Update `GOOGLE_SCRIPT_URL` in index.html
- [ ] (Optional) Add your own music
- [ ] Customize wedding details (names, date, location)
- [ ] Replace hero image
- [ ] Test RSVP form locally
- [ ] Deploy to web (GitHub Pages/Netlify)
- [ ] Share the link with guests!

---

**Congratulations!** Your wedding invitation website is ready. 🎉

_Той кутмандуу болсун! (May your wedding be blessed!)_
