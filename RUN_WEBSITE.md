# 🚀 How to Run the Factory Management System Website

## Step 1: Install Python (if not already installed)

1. **Download Python 3.8+** from [python.org](https://www.python.org/downloads/)
2. **During installation**, check ✅ "Add Python to PATH"
3. **Verify installation:**
   ```powershell
   python --version
   ```

## Step 2: Navigate to Project Directory

```powershell
cd D:\Shrey\i
```

## Step 3: Install Required Packages

```powershell
pip install -r requirements.txt
```

**Expected packages:**
- Flask==3.0.0
- Flask-SQLAlchemy==3.1.1
- Flask-JWT-Extended==4.5.3
- Flask-CORS==4.0.0
- Werkzeug==3.0.1
- python-dotenv==1.0.0
- SQLAlchemy==2.0.36

## Step 4: Run the Website

**Option A - Using run.py:**
```powershell
python run.py
```

**Option B - Using app.py directly:**
```powershell
python app.py
```

**Option C - Using start_server.py:**
```powershell
python start_server.py
```

## Step 5: Access the Website

Once the server starts, you'll see:
```
🚀 Server starting on http://localhost:5000
```

**Open in browser:**
- **Frontend:** http://localhost:5000/
- **API Health Check:** http://localhost:5000/api/health
- **API Info:** http://localhost:5000/api

## Default Login Credentials

- **Username:** `admin`
- **Password:** `password`

OR

- **Username:** `manager`
- **Password:** `password`

## Troubleshooting

### If Port 5000 is Already in Use:

```powershell
# Find process using port 5000
netstat -ano | findstr :5000

# Kill the process (replace <PID> with actual process ID)
taskkill /PID <PID> /F

# Or use a different port
$env:PORT=5001
python run.py
```

### If Dependencies Fail to Install:

```powershell
# Upgrade pip first
python -m pip install --upgrade pip

# Then install requirements
pip install -r requirements.txt

# Or install individually
pip install Flask Flask-SQLAlchemy Flask-JWT-Extended Flask-CORS Werkzeug python-dotenv SQLAlchemy
```

### If Database Errors Occur:

```powershell
# Ensure instance directory exists
mkdir instance

# The database will be created automatically on first run
```

## Stopping the Server

Press `Ctrl+C` in the terminal to stop the server.

---

**Note:** Make sure Python is installed and added to PATH before proceeding!


