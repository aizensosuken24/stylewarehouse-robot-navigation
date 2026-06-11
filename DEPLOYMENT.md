# Deployment Guide

## Frontend Structure

The frontend has been created with HTML/CSS/JavaScript for easy deployment on Vercel:

### File Structure
```
public/
├── index.html           # Main HTML page
├── css/
│   └── styles.css       # All styles (responsive design)
└── js/
    ├── api.js           # API communication module
    ├── visualizer.js    # Warehouse canvas visualization
    └── app.js           # Main application logic
```

### Features

1. **Product Catalogue Search** - Search and browse products from the warehouse catalogue
2. **Order Simulation** - Create custom orders or load demo orders
3. **Warehouse Visualization** - Interactive canvas showing:
   - Warehouse grid layout
   - Robot position
   - Item locations
   - Pathfinding visualization
4. **Real-time Stats** - Display simulation metrics:
   - Total distance traveled
   - Items collected
   - Waypoints
   - Algorithm details

### Deployment Steps

#### 1. Local Testing
```bash
# Install dependencies
pip install -r requirements.txt

# Run the app locally
python app.py

# Visit http://localhost:8000
```

#### 2. Deploy to Vercel

**Option A: Using Vercel CLI**
```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel
```

**Option B: Using GitHub Integration**
1. Push code to GitHub
2. Go to https://vercel.com/import
3. Select your repository
4. Vercel will auto-detect Python and deploy

#### 3. Environment Variables
No environment variables required for basic deployment. The app works with relative URLs.

### API Endpoints

The frontend communicates with these backend endpoints:

- `GET /api/health` - Health check
- `GET /api/catalogue` - Get all products
- `GET /api/catalogue?search=query&limit=20` - Search products
- `GET /api/catalogue/{id}` - Get specific product
- `GET /api/demo-order` - Load demo order
- `POST /api/simulate-order` - Simulate order (expects JSON body with items array)

### Customization

**Styling** - Edit `public/css/styles.css` to customize colors and layout
```css
:root {
    --primary: #2563EB;
    --success: #10B981;
    --danger: #EF4444;
    /* ... more colors ... */
}
```

**API Base URL** - Edit `public/js/api.js` if deploying to different domain
```javascript
const API = {
    baseURL: '', // Use relative URLs for same domain
    // Or specify absolute URL for different domain:
    // baseURL: 'https://api.example.com',
```

### Performance

- Lightweight frontend (~150KB uncompressed)
- No external dependencies
- Responsive design (mobile, tablet, desktop)
- Canvas rendering for efficient visualization
- Caching headers for static files

### Troubleshooting

**CORS Errors**
- The backend includes `Access-Control-Allow-Origin: *` headers
- If still having issues, check that API routes are correctly prefixed with `/api/`

**Canvas not rendering**
- Check browser console for errors
- Ensure warehouse layout data is being returned from backend

**Slow Performance**
- Check network tab in DevTools for slow API calls
- Consider enabling gzip compression in Vercel settings

### Next Steps

- Add real-time path animation in canvas
- Implement WebSocket for live updates
- Add order history tracking
- Create admin dashboard
- Add authentication/login system
