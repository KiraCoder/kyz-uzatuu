# Кыз Узатуу - Wedding Invitation Website

A beautiful, fully-functional wedding invitation website for Aliya's Kyz Uzatuu (traditional Kyrgyz wedding celebration) on August 8, 2026.

## ✨ Features

### Core Features
- 🎨 **Pixel-Perfect Design** - Implemented from Claude Design handoff
- 📱 **Fully Mobile Responsive** - Works perfectly on all devices (320px+)
- 🎵 **Background Music** - Auto-plays on scroll with manual toggle
- ✨ **Scroll Reveal Animations** - Beautiful entrance effects for all sections
- ⏱️ **Live Countdown Timer** - Real-time countdown to the wedding
- 📅 **Interactive Calendar** - August 2026 with highlighted wedding date
- 📍 **Google Maps Integration** - Direct link to venue location
- 📝 **Google Sheets RSVP** - Responses automatically saved to spreadsheet

### RSVP Features
- Name input with placeholder guidance
- Three response options (Coming / Coming with spouse / Cannot attend)
- Form validation with error messages in Kyrgyz
- Loading state during submission
- Thank you confirmation message
- localStorage backup for reliability

### Animation Types
- **Fade In** - Smooth opacity transitions
- **Slide Up** - Elements rise from below
- **Slide Left/Right** - Directional entrance effects
- **Scale In** - Zoom-in effects
- Staggered delays for grouped elements

## 🎨 Design Details

### Colors
- Background: `#FAF9F7` (warm cream)
- Primary Text: `#4C463F` (dark brown)
- Accent: `#9A928B` (taupe)
- Secondary: `#8C837A`, `#5A534C`, `#6E665F`

### Typography
- **Marck Script** - Decorative cursive for titles
- **Cormorant Garamond** - Elegant serif for headings
- **Source Serif 4** - Body text and form elements
- All fonts loaded from Google Fonts CDN

### Layout
- Mobile-first responsive design
- Container max-width: 480px
- Fluid typography using `clamp()`
- Flexible spacing with CSS `clamp()`
- Optimized for screens from 320px to 1920px

## 📋 Sections

1. **Hero** - Full-screen with background image, overlay gradients, music button
2. **Invitation** - Welcome message and event details in Kyrgyz
3. **Calendar** - August 2026 calendar with date 8 highlighted
4. **Address** - Venue location with decorative icon
5. **Countdown** - Days, hours, minutes to the wedding
6. **Hosts** - Wedding hosts with botanical ornaments
7. **RSVP** - Form with Google Sheets integration

## 🚀 Quick Start

### Option 1: Simple Testing
1. Open `index.html` in a web browser
2. Works offline for testing (RSVP won't save without Google Sheets setup)

### Option 2: Full Setup with Google Sheets
See **[SETUP_GUIDE.md](SETUP_GUIDE.md)** for complete instructions including:
- Google Apps Script deployment
- Music file setup
- Customization guide
- Deployment options (GitHub Pages, Netlify, etc.)

## 📁 Project Structure

```
kyz-uzatuu/
├── index.html                  # Main website file
├── images/
│   └── hero-shokulo.png       # Hero background image
├── google-apps-script.js      # Backend code for Google Sheets
├── SETUP_GUIDE.md             # Complete setup instructions
└── README.md                  # This file
```

## 🔧 Configuration

### Required Setup

1. **Google Sheets Integration**:
   - Deploy Google Apps Script (see SETUP_GUIDE.md)
   - Update `GOOGLE_SCRIPT_URL` in index.html (line 1042)

2. **Music File**:
   - Replace music URL in index.html (line 860)
   - Or use the default placeholder

### Optional Customization

1. **Wedding Details**:
   - Bride's name (line 891)
   - Wedding date (line 893, 1125)
   - Hosts names (line 979)
   - Venue location (lines 935-936, 938)

2. **Hero Image**:
   - Replace `images/hero-shokulo.png`
   - Or update image path (line 878)

3. **Colors**:
   - Search and replace color hex codes in CSS

## 🛠️ Technical Implementation

- **Pure HTML/CSS/JavaScript** - No frameworks or build tools
- **Intersection Observer API** - For scroll reveal animations
- **CSS Grid & Flexbox** - Modern layout techniques
- **CSS Custom Properties** - For responsive sizing
- **Fetch API** - For RSVP submission to Google Sheets
- **LocalStorage API** - Backup storage for submissions
- **Audio API** - Background music with autoplay handling

## 📊 RSVP Data Structure

Responses are saved to Google Sheets with:
- Timestamp
- Guest name(s)
- Response status (Kyrgyz + code)
- User agent (for troubleshooting)

## 🌐 Browser Support

- ✅ Chrome/Edge 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ iOS Safari 14+
- ✅ Chrome Mobile 90+

## 🎯 Performance

- Minimal dependencies (only Google Fonts)
- Lazy-loaded animations (Intersection Observer)
- Optimized images
- No external JavaScript libraries
- Fast initial load time

## 📱 Mobile Optimization

- Touch-friendly buttons (44px+ touch targets)
- Responsive typography
- Optimized for 320px - 768px screens
- Works in both portrait and landscape
- No horizontal scrolling

## 🔐 Privacy & Security

- No cookies used
- No user tracking
- Optional localStorage for backup only
- Google Sheets access controlled via Apps Script
- No sensitive data stored client-side

## 🎭 Accessibility

- Semantic HTML5 markup
- ARIA labels for interactive elements
- Keyboard navigation support
- Screen reader friendly
- Sufficient color contrast ratios

## 📄 License

This is a custom wedding invitation. Feel free to use as a template for your own wedding.

## 🙏 Credits

**Implemented from Claude Design handoff**
- Original design: `kyrgyz-wedding-invitation-design/project/Kyz Uzatuu.dc.html`
- Fonts: Google Fonts (Marck Script, Cormorant Garamond, Source Serif 4)
- Icons: Custom SVG botanical ornaments

---

**Той кутмандуу болсун!** (May your wedding be blessed!)

For detailed setup instructions, see **[SETUP_GUIDE.md](SETUP_GUIDE.md)**
