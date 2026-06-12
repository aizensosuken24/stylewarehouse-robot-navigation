/**
 * Warehouse Visualization Module
 * Handles canvas rendering of warehouse layout and robot path
 */

class WarehouseVisualizer {
    constructor(canvasId, warehouseLayout) {
        this.canvas = document.getElementById(canvasId);
        if (!this.canvas) {
            console.error('Canvas element not found:', canvasId);
            return;
        }
        this.ctx = this.canvas.getContext('2d');
        this.layout = warehouseLayout;
        this.robot = null;
        this.path = [];
        this.items = [];
        this.cellSize = 40;
        this.padding = 30;
        try {
            this.setupCanvas();
        } catch (e) {
            console.error('Error setting up canvas:', e);
        }
    }

    setupCanvas() {
        // Set canvas to fill its container
        const wrapper = this.canvas.parentElement;
        if (!wrapper) {
            console.error('Canvas parent element not found');
            this.canvas.width = 800;
            this.canvas.height = 600;
        } else {
            this.canvas.width = Math.max(wrapper.offsetWidth - 40, 400); // Accounting for padding
            this.canvas.height = Math.min(600, wrapper.offsetHeight || 600);
        }
        this.draw();
    }

    setRobotPosition(x, y) {
        this.robot = { x, y };
    }

    setPath(pathArray) {
        this.path = pathArray || [];
    }

    setItems(itemLocations) {
        this.items = itemLocations || [];
    }

    draw() {
        // Clear canvas
        this.ctx.fillStyle = '#F9FAFB';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

        if (!this.layout) {
            this.drawDefaultGrid();
        } else {
            this.drawLayout();
        }

        // Draw path
        this.drawPath();

        // Draw items
        this.drawItems();

        // Draw robot
        if (this.robot) {
            this.drawRobot(this.robot.x, this.robot.y);
        }
    }

    drawDefaultGrid() {
        const cols = 10;
        const rows = 8;

        // Draw grid lines
        this.ctx.strokeStyle = '#E5E7EB';
        this.ctx.lineWidth = 1;

        for (let i = 0; i <= cols; i++) {
            const x = this.padding + i * this.cellSize;
            this.ctx.beginPath();
            this.ctx.moveTo(x, this.padding);
            this.ctx.lineTo(x, this.padding + rows * this.cellSize);
            this.ctx.stroke();
        }

        for (let i = 0; i <= rows; i++) {
            const y = this.padding + i * this.cellSize;
            this.ctx.beginPath();
            this.ctx.moveTo(this.padding, y);
            this.ctx.lineTo(this.padding + cols * this.cellSize, y);
            this.ctx.stroke();
        }

        // Draw labels
        this.ctx.fillStyle = '#6B7280';
        this.ctx.font = '12px sans-serif';
        this.ctx.textAlign = 'center';
        this.ctx.textBaseline = 'middle';

        // Column labels (A, B, C, ...)
        for (let i = 0; i < cols; i++) {
            const x = this.padding + i * this.cellSize + this.cellSize / 2;
            this.ctx.fillText(i + 1, x, this.padding - 10);
        }

        // Row labels (1, 2, 3, ...)
        for (let i = 0; i < rows; i++) {
            const y = this.padding + i * this.cellSize + this.cellSize / 2;
            this.ctx.fillText(String.fromCharCode(65 + i), this.padding - 10, y);
        }
    }

    drawLayout() {
        // Draw warehouse layout if provided
        // This is a placeholder for custom layout rendering
        this.drawDefaultGrid();
    }

    drawPath() {
        if (this.path.length < 2) return;

        this.ctx.strokeStyle = '#95E1D3';
        this.ctx.lineWidth = 2;
        this.ctx.setLineDash([5, 5]);

        this.ctx.beginPath();
        let firstPoint = true;

        for (const point of this.path) {
            const { x, y } = this.gridToCanvas(point.x, point.y);
            if (firstPoint) {
                this.ctx.moveTo(x, y);
                firstPoint = false;
            } else {
                this.ctx.lineTo(x, y);
            }
        }

        this.ctx.stroke();
        this.ctx.setLineDash([]);
    }

    drawItems() {
        for (const item of this.items) {
            const { x, y } = this.gridToCanvas(item.col, item.row);

            // Draw item marker
            this.ctx.fillStyle = '#FFE66D';
            this.ctx.beginPath();
            this.ctx.arc(x, y, 8, 0, Math.PI * 2);
            this.ctx.fill();

            // Draw border
            this.ctx.strokeStyle = '#F59E0B';
            this.ctx.lineWidth = 2;
            this.ctx.stroke();

            // Draw label
            this.ctx.fillStyle = '#92400E';
            this.ctx.font = 'bold 10px sans-serif';
            this.ctx.textAlign = 'center';
            this.ctx.textBaseline = 'middle';
            this.ctx.fillText(item.id.slice(-3), x, y);
        }
    }

    drawRobot(gridX, gridY) {
        const { x, y } = this.gridToCanvas(gridX, gridY);

        // Draw robot body
        this.ctx.fillStyle = '#4ECDC4';
        this.ctx.fillRect(x - 12, y - 12, 24, 24);

        // Draw robot border
        this.ctx.strokeStyle = '#1A9D8F';
        this.ctx.lineWidth = 2;
        this.ctx.strokeRect(x - 12, y - 12, 24, 24);

        // Draw robot eyes
        this.ctx.fillStyle = '#1A9D8F';
        this.ctx.fillRect(x - 8, y - 8, 4, 4);
        this.ctx.fillRect(x + 4, y - 8, 4, 4);
    }

    gridToCanvas(gridX, gridY) {
        const x = this.padding + gridX * this.cellSize + this.cellSize / 2;
        const y = this.padding + gridY * this.cellSize + this.cellSize / 2;
        return { x, y };
    }

    canvasToGrid(canvasX, canvasY) {
        const gridX = Math.floor((canvasX - this.padding) / this.cellSize);
        const gridY = Math.floor((canvasY - this.padding) / this.cellSize);
        return { x: gridX, y: gridY };
    }

    update(simulationData) {
        if (!simulationData) return;

        // Parse robot path
        if (simulationData.path) {
            this.setPath(simulationData.path);
        }

        // Parse item locations
        if (simulationData.items && Array.isArray(simulationData.items)) {
            const items = simulationData.items.map(item => {
                const loc = parseLocation(item.location);
                return {
                    id: item.id,
                    row: loc ? loc.row : 0,
                    col: loc ? loc.col : 0,
                };
            });
            this.setItems(items);
        }

        // Set robot start position
        if (simulationData.start_position) {
            const loc = parseLocation(simulationData.start_position);
            if (loc) {
                this.setRobotPosition(loc.col, loc.row);
            }
        }

        this.draw();
    }

    clear() {
        this.robot = null;
        this.path = [];
        this.items = [];
        this.draw();
    }
}

// Handle window resize for responsive canvas
let visualizer = null;
window.addEventListener('resize', () => {
    if (visualizer) {
        visualizer.setupCanvas();
    }
});
