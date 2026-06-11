# Frontend - Quick Reference

## Created Files Summary

### HTML Structure
- **public/index.html** (430 lines)
  - Complete responsive UI with 6 main sections
  - Catalogue search interface
  - Order simulation controls
  - Warehouse visualization canvas
  - Real-time stats display
  - Response data viewer

### Styling
- **public/css/styles.css** (620 lines)
  - Modern design with gradient background
  - Responsive grid layouts
  - Card-based components
  - Mobile, tablet, and desktop breakpoints
  - Smooth animations and transitions
  - Dark code block for JSON responses

### JavaScript Modules

#### 1. **public/js/api.js** - API Communication
- `API.health()` - Check backend connectivity
- `API.getCatalogue()` - Fetch all products
- `API.searchCatalogue(query, limit)` - Search products
- `API.getProduct(productId)` - Get single product
- `API.getDemoOrder()` - Load demo order
- `API.simulateOrder(items)` - Run order simulation

Helper functions:
- `formatJSON(obj, indent)` - Pretty-print JSON
- `parseLocation(location)` - Parse "A1" format to coordinates
- `formatLocation(row, col)` - Convert coordinates to "A1" format

#### 2. **public/js/visualizer.js** - Canvas Visualization
`WarehouseVisualizer` class:
- Constructor initializes canvas and layout
- `setRobotPosition(x, y)` - Position robot
- `setPath(pathArray)` - Show navigation path
- `setItems(itemLocations)` - Mark item locations
- `draw()` - Render everything
- `update(simulationData)` - Update from simulation response
- `clear()` - Reset visualization

Renders:
- Grid layout with coordinates (A1, A2, etc.)
- Robot as blue square with eyes
- Items as yellow circles with IDs
- Path as dashed teal line
- Legend with color meanings

#### 3. **public/js/app.js** - Main Logic
Global state:
- `state.catalogue` - Product list
- `state.selectedItems` - Current order
- `state.currentSimulation` - Last simulation result

Key functions:
- `init()` - Initialize app and load data
- `loadCatalogue()` - Load all products
- `searchCatalogue()` - Search products
- `displayCatalogue()` - Render product grid
- `toggleItemSelection()` - Add/remove items
- `loadDemoOrder()` - Load example order
- `runSimulation()` - Execute order routing
- `updateSimulationStats()` - Display metrics
- `clearOrder()` - Reset everything

## UI Sections

### 1. Header
- Title and subtitle
- Health status indicator (● Connected/Disconnected)

### 2. Catalogue Section
- Search input with search, clear buttons
- Product grid (3-4 columns responsive)
- Click product to select/deselect
- Shows: ID, name, location, quantity

### 3. Order Section
- Demo Order, Simulate, Clear buttons
- Split view:
  - Left: Selected items list with remove buttons
  - Right: Order summary (total items, locations, category)

### 4. Visualization Section
- Canvas (800x600px, responsive)
- Legend showing colors
- Stats card: distance, items, waypoints, algorithm
- Pathfinding details: start, end, distance, execution time

### 5. Response Section
- Raw JSON display of last response
- Dark code block with scrolling
- Useful for debugging

### 6. Footer
- Copyright and tech info

## How It Works

### Flow Diagram
```
1. App loads → Check health → Load catalogue
2. User searches or browses products
3. User clicks products to select (highlighted)
4. User clicks "Simulate Order"
5. API executes order routing
6. Response updates:
   - Visualization canvas
   - Statistics
   - Response data viewer
```

### Data Flow
```
Frontend                    Backend
├─ Search input     ────→   /api/catalogue?search=...
│                   ←────   {items: [...]}
│
├─ Select items     ────→   (stored locally)
│
└─ Simulate Order   ────→   /api/simulate-order (POST)
                    ←────   {path, items, distance, ...}
                           │
                           └─→ Visualizer updates
                               Stats update
                               Response displayed
```

## Responsive Breakpoints

- **Desktop**: 1400px+ (2-column layouts)
- **Tablet**: 768-1024px (1-column layouts)
- **Mobile**: <768px (stacked, full-width buttons)

## Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile browsers (iOS Safari, Chrome Mobile)

## Features Highlights

✅ No external dependencies (vanilla JS)
✅ Real-time API communication
✅ Interactive canvas visualization  
✅ Responsive design
✅ Dark/light compatible
✅ Performance optimized
✅ Accessible HTML structure
✅ CORS-enabled for cross-origin requests

## Development Tips

### Testing Locally
```bash
# Terminal 1: Start backend
python app.py

# Terminal 2: Open browser
# http://localhost:8000
```

### Common Issues & Solutions

**Search doesn't work**
- Check API response in Network tab
- Verify query parameter format

**Visualization not showing**
- Check console for JavaScript errors
- Verify path data format from API

**Slow performance**
- Check Network tab for slow API calls
- Reduce catalogue size in search limit

### Customization Examples

Change primary color:
```css
:root {
    --primary: #FF0000; /* Change to red */
}
```

Add new metric display:
```javascript
elements.customStat = document.getElementById('custom-stat');
// In updateSimulationStats:
elements.customStat.textContent = data.custom_value;
```

Modify canvas grid size:
```javascript
visualizer.cellSize = 50; // Was 40
visualizer.padding = 50;  // Was 30
visualizer.draw();
```
