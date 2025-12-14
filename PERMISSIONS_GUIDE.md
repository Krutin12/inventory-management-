# Factory Management System - Role-Based Permissions

## User Roles and Permissions

### 🔧 **MANAGER ROLE**
**Username:** `manager`  
**Password:** `password`

**Permissions:**
- ✅ **View** - Can view all data (orders, inventory, etc.)
- ✅ **Edit** - Can edit existing orders and inventory
- ✅ **New Order** - Can create new orders
- ❌ **User Management** - NO access to user management
- ❌ **Admin Features** - NO access to admin-only features

**What Manager CANNOT do:**
- Add/Edit/Delete users
- Access admin dashboard
- Manage user accounts
- Access admin-only navigation

---

### 👑 **ADMIN ROLE**
**Username:** `admin`  
**Password:** `password`

**Permissions:**
- ✅ **Full Access** - All features available
- ✅ **User Management** - Can add/edit/delete users
- ✅ **Admin Dashboard** - Full admin dashboard access
- ✅ **All Features** - Complete system access

**What Admin CAN do:**
- Everything Manager can do
- Plus: User management
- Plus: Admin dashboard
- Plus: All system features

---

## How to Test

1. **Start the server:**
   ```bash
   py run_working.py
   ```

2. **Open browser:** `http://localhost:5000`

3. **Test Manager Login:**
   - Username: `manager`
   - Password: `password`
   - Role will auto-select: `manager`
   - Notice: NO "Users" tab visible

4. **Test Admin Login:**
   - Username: `admin`
   - Password: `password`
   - Role will auto-select: `admin`
   - Notice: "Users" tab is visible

---

## Technical Implementation

### Frontend (HTML/JavaScript)
- Role-based UI hiding/showing
- Permission checks before actions
- Auto role selection based on username
- Visual indicators for current role

### Backend (Python/Flask)
- Secure authentication
- Role validation
- API endpoints with proper responses
- No database dependency issues

---

## Security Features

✅ **Authentication Required** - Must login to access system  
✅ **Role Validation** - Server validates user role  
✅ **UI Restrictions** - Frontend hides unauthorized features  
✅ **API Protection** - Backend enforces permissions  
✅ **Session Management** - Proper login/logout handling  

---

## Quick Start

```bash
# Start the server
py run_working.py

# Open browser to:
http://localhost:5000

# Login with:
# Manager: manager/password
# Admin: admin/password
```

The system will automatically apply the correct permissions based on the user's role!
