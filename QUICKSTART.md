# 🚀 Quick Start Guide

## 30-Second Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Application
```bash
python app.py
```

### 3. Open Browser
```
http://localhost:5000
```

### 4. Login
- **Username:** `admin` or `user`
- **Password:** `admin123` or `user123`

---

## 🎯 What You Get

✅ **Professional Dashboard** with real-time metrics  
✅ **Admin Panel** for system management  
✅ **Data Export** in CSV/JSON format  
✅ **Mobile Responsive** design  
✅ **Secure Authentication** with login  
✅ **Live Charts** with Apex Charts  
✅ **Alert System** for faults  

---

## 📍 Key Pages

| URL | Purpose |
|-----|---------|
| `http://localhost:5000` | Main Dashboard |
| `http://localhost:5000/admin` | Admin Panel (admin only) |
| `http://localhost:5000/export` | Data Export |
| `http://localhost:5000/logout` | Logout |

---

## 🔧 First-Time Configuration

**IMPORTANT:** Change the secret key in `app.py` line 8:

```python
# BEFORE (NOT SECURE)
app.secret_key = "your-secret-key-change-this"

# AFTER (EXAMPLE)
app.secret_key = "my_ultra_secure_key_xyz123"
```

---

## 📊 Dashboard Features

### Real-Time Metrics
- Voltage (V)
- Current (mA)
- Frequency (Hz)
- System Status

### Charts
- Voltage Trend
- Current Trend
- Frequency Trend
- System Health Radar

### Data Management
- Live data table
- Auto-refresh every 5 seconds
- Training visualizations
- Model accuracy comparison

---

## 👤 Demo Accounts

```
Admin Account:
├─ Username: admin
├─ Password: admin123
└─ Access: Full admin panel

User Account:
├─ Username: user
├─ Password: user123
└─ Access: Dashboard and export only
```

---

## 🛑 If Something Goes Wrong

### Flask won't start?
```bash
# Check if port is in use
# If yes, try different port:
# Change port=5000 to port=5001 in app.py
```

### Missing module?
```bash
# Reinstall all dependencies
pip install --upgrade -r requirements.txt
```

### Clear cache
```bash
# Window users: Press Ctrl+Shift+Delete in browser
# Then select "All time" and "Cookies" and "Images"
```

---

## 📚 Full Documentation

See **SETUP_GUIDE.md** for complete documentation including:
- Detailed feature explanations
- Configuration options
- Troubleshooting guide
- Customization ideas
- Security best practices

---

**You're ready to go!** Start with `python app.py` 🚀
