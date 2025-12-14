# 🐛 Bug Report and Fixes

This document identifies all the bugs found and provides solutions for each issue.

---

## ❌ BUG #1: Inventory Stock Add/Edit Not Working

### Problem:
The inventory stock adjustment functionality only updates the DOM locally but doesn't save changes to the backend database. When you add or edit stock, the changes appear temporarily but are lost when the page refreshes.

### Root Cause:
The `saveStockAdjustment()` function in `1.html` (line 5679) only updates the HTML table locally:
```javascript
function saveStockAdjustment(itemId) {
    // ... only updates DOM, doesn't call API
    row.setAttribute('data-stock', newStock.toString());
    // Missing: API call to /api/inventory/<item_id>/adjust
}
```

### Solution:
Update the `saveStockAdjustment()` function to call the backend API:

**Location:** `1.html` around line 5679

**Change from:**
```javascript
function saveStockAdjustment(itemId) {
    const adjustmentType = document.getElementById('adjustmentType').value;
    const quantity = parseInt(document.getElementById('adjustmentQuantity').value) || 0;
    const reason = document.getElementById('adjustmentReason').value;
    
    // ... only DOM updates ...
    
    showNotification(`Stock updated for ${itemId}. New quantity: ${newStock}`, 'success');
    updateInventoryStats();
}
```

**Change to:**
```javascript
function saveStockAdjustment(itemId) {
    const adjustmentType = document.getElementById('adjustmentType').value;
    const quantity = parseFloat(document.getElementById('adjustmentQuantity').value) || 0;
    const reason = document.getElementById('adjustmentReason').value;
    
    if (quantity <= 0) {
        showNotification('Please enter a valid quantity', 'error');
        return;
    }
    
    if (!reason.trim()) {
        showNotification('Please enter a reason for the adjustment', 'error');
        return;
    }
    
    // Map 'set' to 'adjust' for API compatibility
    const movementType = adjustmentType === 'set' ? 'adjust' : adjustmentType;
    
    // Call backend API
    fetch(`/api/inventory/${itemId}/adjust`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${getAuthToken()}`
        },
        body: JSON.stringify({
            movement_type: movementType,
            quantity: quantity,
            reason: reason
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            showNotification(`Error: ${data.error}`, 'error');
            return;
        }
        
        // Update the DOM with the response
        const row = document.querySelector(`tr[data-item-id="${itemId}"]`);
        if (row && data.item) {
            row.setAttribute('data-stock', data.item.current_stock);
            const stockCell = row.querySelector('td:nth-child(4) strong');
            if (stockCell) {
                stockCell.textContent = data.item.current_stock;
                // Update status colors
                const minLevel = parseInt(row.getAttribute('data-min')) || 0;
                if (data.item.current_stock === 0) {
                    stockCell.style.color = '#ef4444';
                } else if (data.item.current_stock < minLevel) {
                    stockCell.style.color = '#f59e0b';
                } else {
                    stockCell.style.color = '#10b981';
                }
            }
            
            // Update status badge
            const statusBadge = row.querySelector('.status-badge');
            if (statusBadge) {
                if (data.item.status === 'out-of-stock') {
                    statusBadge.textContent = '✗ Out of Stock';
                    statusBadge.className = 'status-badge';
                    statusBadge.style.background = '#fecaca';
                    statusBadge.style.color = '#991b1b';
                } else if (data.item.status === 'low-stock') {
                    statusBadge.textContent = '⚠️ Low Stock';
                    statusBadge.className = 'status-badge status-pending';
                } else {
                    statusBadge.textContent = '✓ In Stock';
                    statusBadge.className = 'status-badge status-ready';
                }
            }
        }
        
        showNotification(`Stock updated successfully. New quantity: ${data.item.current_stock}`, 'success');
        updateInventoryStats();
        
        // Reload inventory list to get fresh data
        loadInventoryList();
    })
    .catch(error => {
        console.error('Error updating stock:', error);
        showNotification('Failed to update stock. Please try again.', 'error');
    });
}
```

**Also add this helper function if missing:**
```javascript
function getAuthToken() {
    return localStorage.getItem('access_token') || '';
}
```

---

## ❌ BUG #2: ID Not Auto-Generated in Add Forms

### Problem:
When clicking "Add Item" in the inventory page, the Item Code field shows "Auto-generated" but doesn't actually generate an ID automatically. Users have to manually enter an ID.

### Root Cause:
The `showAddInventoryForm()` function is called but likely missing or doesn't generate the ID. The form field `formItemCode` needs to be populated when the form is shown.

### Solution:

**Location:** `1.html` - Add this function if missing, or update if it exists

**Add/Update the `showAddInventoryForm()` function:**

```javascript
function showAddInventoryForm() {
    // Show the form view
    document.getElementById('inventoryListView').style.display = 'none';
    document.getElementById('inventoryFormView').style.display = 'block';
    document.getElementById('inventoryDetailView').style.display = 'none';
    
    // Reset form
    document.getElementById('inventoryDetailsForm').reset();
    
    // Generate and set item code
    // Note: In production, you'd fetch this from the API or generate it on the server
    // For now, generate a client-side ID
    const itemCode = generateInventoryItemCode();
    document.getElementById('formItemCode').value = itemCode;
    
    // Update form title
    document.getElementById('inventoryFormTitle').textContent = 'Add New Item';
    document.getElementById('inventoryFormCardTitle').textContent = 'Item Details';
    
    // Set submit button text
    const submitBtn = document.getElementById('inventoryFormSubmit');
    if (submitBtn) {
        submitBtn.textContent = 'Add Item';
    }
}

function generateInventoryItemCode() {
    // Try to get the highest existing ID from the table
    const rows = document.querySelectorAll('#inventoryTable tbody tr[data-item-id]');
    let maxNum = 0;
    
    rows.forEach(row => {
        const itemId = row.getAttribute('data-item-id');
        if (itemId && itemId.startsWith('ITM-')) {
            const num = parseInt(itemId.split('-')[1]);
            if (num > maxNum) maxNum = num;
        }
    });
    
    // Generate new ID
    const newNum = maxNum + 1;
    return `ITM-${String(newNum).padStart(4, '0')}`;
}
```

**Better solution - Get ID from API:**
The backend generates IDs automatically, so update the form submission to handle this:

```javascript
function showAddInventoryForm() {
    // Show the form view
    document.getElementById('inventoryListView').style.display = 'none';
    document.getElementById('inventoryFormView').style.display = 'block';
    document.getElementById('inventoryDetailView').style.display = 'none';
    
    // Reset form
    document.getElementById('inventoryDetailsForm').reset();
    
    // Set placeholder - ID will be generated by backend
    document.getElementById('formItemCode').value = '';
    document.getElementById('formItemCode').placeholder = 'Auto-generated by server';
    
    // Update form title
    document.getElementById('inventoryFormTitle').textContent = 'Add New Item';
    document.getElementById('inventoryFormCardTitle').textContent = 'Item Details';
}
```

**And update the form submission to use the API:**

**Location:** Find or add form submission handler around line 3800+

```javascript
// Add form submission handler for inventory
document.getElementById('inventoryDetailsForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const formData = {
        item_name: document.getElementById('formItemName').value,
        category: document.getElementById('formCategory').value,
        current_stock: parseFloat(document.getElementById('formCurrentStock').value) || 0,
        min_level: parseFloat(document.getElementById('formMinLevel').value) || 0,
        max_level: parseFloat(document.getElementById('formMaxLevel').value) || 0,
        unit: document.getElementById('formUnit').value,
        description: document.getElementById('formDescription').value,
        supplier: document.getElementById('formSupplier').value,
        unit_cost: parseFloat(document.getElementById('formUnitCost').value) || null,
        location: document.getElementById('formLocation').value
    };
    
    // Validate required fields
    if (!formData.item_name || !formData.category || !formData.unit) {
        showNotification('Please fill in all required fields!', 'error');
        return;
    }
    
    // Call API to create inventory item
    fetch('/api/inventory', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${getAuthToken()}`
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            showNotification(`Error: ${data.error}`, 'error');
            return;
        }
        
        showNotification(`Item ${data.item.item_code} created successfully!`, 'success');
        
        // Reload inventory list
        loadInventoryList();
        
        // Return to list view
        showInventoryList();
    })
    .catch(error => {
        console.error('Error creating item:', error);
        showNotification('Failed to create item. Please try again.', 'error');
    });
});
```

---

## ❌ BUG #3: Order Report Not Generating or Downloading PDF

### Problem:
1. The "Generate Order Report" button shows hardcoded sample data instead of fetching real orders from the API
2. The "Download PDF" button doesn't actually generate or download a PDF file - it just shows a notification

### Root Cause:
- `generateOrderReport()` function (line 3914) uses hardcoded sample data instead of calling `/api/reports/orders`
- `downloadOrderReport()` function (line 4057) is just a placeholder that doesn't create a PDF

### Solution:

**Fix 1: Update `generateOrderReport()` to use API:**

**Location:** `1.html` around line 3914

**Change from:**
```javascript
function generateOrderReport() {
    const reportType = document.getElementById('orderReportType').value;
    const fromDate = document.getElementById('orderReportFromDate').value;
    const toDate = document.getElementById('orderReportToDate').value;
    const customerFilter = document.getElementById('orderReportCustomer').value;
    
    // Show loading state
    showNotification('Generating order report...', 'success');
    
    // Simulate report generation
    setTimeout(() => {
        displayOrderReport(reportType, { fromDate, toDate, customerFilter });
        document.getElementById('downloadOrderPDF').disabled = false;
        document.getElementById('downloadOrderExcel').disabled = false;
        showNotification('Order report generated successfully!', 'success');
    }, 1500);
}
```

**Change to:**
```javascript
function generateOrderReport() {
    const reportType = document.getElementById('orderReportType').value;
    const fromDate = document.getElementById('orderReportFromDate').value;
    const toDate = document.getElementById('orderReportToDate').value;
    const customerFilter = document.getElementById('orderReportCustomer').value;
    
    // Show loading state
    showNotification('Generating order report...', 'info');
    
    // Build API query parameters
    const params = new URLSearchParams();
    if (fromDate) params.append('start_date', fromDate);
    if (toDate) params.append('end_date', toDate);
    if (reportType && reportType !== 'all') params.append('status', reportType);
    
    // Call API to get order report
    fetch(`/api/reports/orders?${params.toString()}`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${getAuthToken()}`
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            showNotification(`Error: ${data.error}`, 'error');
            return;
        }
        
        // Store report data for PDF generation
        window.currentOrderReport = data;
        
        // Display the report
        displayOrderReportFromAPI(data, { fromDate, toDate, customerFilter });
        
        // Enable download buttons
        document.getElementById('downloadOrderPDF').disabled = false;
        document.getElementById('downloadOrderExcel').disabled = false;
        
        showNotification(`Order report generated successfully! Found ${data.orders.length} orders.`, 'success');
    })
    .catch(error => {
        console.error('Error generating report:', error);
        showNotification('Failed to generate report. Please try again.', 'error');
    });
}
```

**Fix 2: Update `displayOrderReport()` to use real data:**

**Location:** `1.html` around line 3932

**Change from:**
```javascript
function displayOrderReport(reportType, filters) {
    document.getElementById('reportResults').style.display = 'block';
    document.getElementById('reportTitle').textContent = `Order Report - ${reportType.replace('-', ' ').toUpperCase()}`;
    
    // Sample report data
    const reportData = [
        { id: 'ORD-001', customer: 'ABC Industries', product: 'Steel Pipes', quantity: 500, amount: '$12,500', status: 'Under Process', date: '2025-09-20' },
        // ... hardcoded data
    ];
    
    // ... rest of display code
}
```

**Change to:**
```javascript
function displayOrderReportFromAPI(apiData, filters) {
    document.getElementById('reportResults').style.display = 'block';
    
    const reportType = filters.reportType || 'All Orders';
    document.getElementById('reportTitle').textContent = `Order Report - ${reportType.toUpperCase()}`;
    
    const orders = apiData.orders || [];
    const summary = apiData.summary || {};
    
    // Update stats
    document.getElementById('reportStats').innerHTML = `
        <div class="stat-card" style="border-left-color: #3b82f6;">
            <div class="stat-number">${summary.total_orders || 0}</div>
            <div class="stat-label">Total Orders</div>
        </div>
        <div class="stat-card" style="border-left-color: #10b981;">
            <div class="stat-number">$${(summary.total_amount || 0).toLocaleString()}</div>
            <div class="stat-label">Total Value</div>
        </div>
        <div class="stat-card" style="border-left-color: #f59e0b;">
            <div class="stat-number">${summary.total_quantity || 0}</div>
            <div class="stat-label">Total Quantity</div>
        </div>
    `;
    
    // Update table
    document.getElementById('reportTableHead').innerHTML = `
        <tr>
            <th>Order ID</th>
            <th>Customer</th>
            <th>Product</th>
            <th>Quantity</th>
            <th>Amount</th>
            <th>Status</th>
            <th>Deadline</th>
            <th>Date</th>
        </tr>
    `;
    
    document.getElementById('reportTableBody').innerHTML = orders.map(order => `
        <tr>
            <td><strong>${order.order_id}</strong></td>
            <td>${order.customer_name}</td>
            <td>${order.product}</td>
            <td>${order.quantity}</td>
            <td><strong>$${(order.total_amount || 0).toFixed(2)}</strong></td>
            <td><span class="status-badge">${order.status}</span></td>
            <td>${order.deadline || 'N/A'}</td>
            <td>${order.created_at ? order.created_at.split('T')[0] : 'N/A'}</td>
        </tr>
    `).join('');
    
    if (orders.length === 0) {
        document.getElementById('reportTableBody').innerHTML = `
            <tr>
                <td colspan="8" style="text-align: center; padding: 40px; color: #64748b;">
                    No orders found for the selected criteria
                </td>
            </tr>
        `;
    }
}
```

**Fix 3: Implement actual PDF download:**

**Location:** `1.html` around line 4057

**Change from:**
```javascript
function downloadOrderReport(format) {
    showNotification(`Downloading order report as ${format.toUpperCase()}...`, 'success');
    // In a real application, this would trigger a file download
    setTimeout(() => {
        showNotification(`Order report downloaded successfully as ${format.toUpperCase()}!`, 'success');
    }, 1000);
}
```

**Change to:**
```javascript
function downloadOrderReport(format) {
    if (!window.currentOrderReport) {
        showNotification('Please generate a report first!', 'error');
        return;
    }
    
    showNotification(`Generating ${format.toUpperCase()} report...`, 'info');
    
    if (format === 'pdf') {
        generatePDFReport(window.currentOrderReport);
    } else if (format === 'excel') {
        generateExcelReport(window.currentOrderReport);
    }
}

function generatePDFReport(reportData) {
    // Use a PDF library like jsPDF or create a printable HTML version
    // Option 1: Use jsPDF (requires adding library to HTML)
    // Option 2: Create a printable HTML page and trigger print
    
    const printContent = generateReportHTML(reportData);
    const printWindow = window.open('', '_blank');
    printWindow.document.write(printContent);
    printWindow.document.close();
    
    // Trigger print dialog (which can save as PDF)
    setTimeout(() => {
        printWindow.print();
        showNotification('PDF generation ready. Use browser print dialog to save as PDF.', 'success');
    }, 500);
}

function generateExcelReport(reportData) {
    // Create CSV format (simpler than Excel, but works)
    const orders = reportData.orders || [];
    const summary = reportData.summary || {};
    
    let csv = 'Order Report\n\n';
    csv += 'Order ID,Customer,Product,Quantity,Amount,Status,Deadline,Date\n';
    
    orders.forEach(order => {
        csv += `"${order.order_id}","${order.customer_name}","${order.product}",${order.quantity},"$${(order.total_amount || 0).toFixed(2)}","${order.status}","${order.deadline || ''}","${order.created_at ? order.created_at.split('T')[0] : ''}"\n`;
    });
    
    csv += `\nSummary\n`;
    csv += `Total Orders,${summary.total_orders || 0}\n`;
    csv += `Total Quantity,${summary.total_quantity || 0}\n`;
    csv += `Total Amount,$${(summary.total_amount || 0).toFixed(2)}\n`;
    
    // Create download link
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    
    link.setAttribute('href', url);
    link.setAttribute('download', `order_report_${new Date().toISOString().split('T')[0]}.csv`);
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    showNotification('Excel report downloaded successfully!', 'success');
}

function generateReportHTML(reportData) {
    const orders = reportData.orders || [];
    const summary = reportData.summary || {};
    
    let html = `
        <!DOCTYPE html>
        <html>
        <head>
            <title>Order Report</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                h1 { color: #1e40af; }
                table { width: 100%; border-collapse: collapse; margin: 20px 0; }
                th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
                th { background-color: #f8fafc; font-weight: bold; }
                .summary { margin: 20px 0; padding: 15px; background: #f8fafc; border-radius: 8px; }
            </style>
        </head>
        <body>
            <h1>Factory Management System - Order Report</h1>
            <div class="summary">
                <strong>Summary:</strong><br>
                Total Orders: ${summary.total_orders || 0}<br>
                Total Quantity: ${summary.total_quantity || 0}<br>
                Total Amount: $${(summary.total_amount || 0).toFixed(2)}<br>
                Generated: ${new Date().toLocaleString()}
            </div>
            <table>
                <thead>
                    <tr>
                        <th>Order ID</th>
                        <th>Customer</th>
                        <th>Product</th>
                        <th>Quantity</th>
                        <th>Amount</th>
                        <th>Status</th>
                        <th>Deadline</th>
                        <th>Date</th>
                    </tr>
                </thead>
                <tbody>
    `;
    
    orders.forEach(order => {
        html += `
            <tr>
                <td>${order.order_id}</td>
                <td>${order.customer_name}</td>
                <td>${order.product}</td>
                <td>${order.quantity}</td>
                <td>$${(order.total_amount || 0).toFixed(2)}</td>
                <td>${order.status}</td>
                <td>${order.deadline || 'N/A'}</td>
                <td>${order.created_at ? order.created_at.split('T')[0] : 'N/A'}</td>
            </tr>
        `;
    });
    
    html += `
                </tbody>
            </table>
        </body>
        </html>
    `;
    
    return html;
}
```

---

## 📝 Summary of Required Changes

1. **Fix Inventory Stock Adjustment** - Update `saveStockAdjustment()` to call `/api/inventory/<id>/adjust` API
2. **Fix ID Generation** - Add/update `showAddInventoryForm()` to generate or fetch item codes
3. **Fix Form Submission** - Add form submission handler that calls `/api/inventory` POST endpoint
4. **Fix Report Generation** - Update `generateOrderReport()` to call `/api/reports/orders` API
5. **Fix PDF Download** - Implement actual PDF/Excel generation in `downloadOrderReport()`

---

## ⚠️ Additional Notes

- All API calls require authentication token - ensure `getAuthToken()` function exists
- Make sure the backend API endpoints are working correctly
- Test each fix individually to ensure they work as expected
- Consider adding loading indicators for better UX during API calls

