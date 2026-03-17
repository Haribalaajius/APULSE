# Smart Grid Dashboard - SETUP & DEPLOYMENT GUIDE

## ✅ SYSTEM STATUS

### Completed Components
1. **Flask Backend** (`app.py`)
   - ✅ Main dashboard route: `/`
   - ✅ User authentication with login/logout
   - ✅ All page routes: /analytics, /models, /alerts, /settings, /admin, /export
   - ✅ All API endpoints working:
     - POST `/api/hardware/data` - Receives sensor data from ESP32
     - GET `/api/analytics` - Returns analytics statistics  
     - GET `/api/alerts` - Returns fault alerts
     - GET `/api/hardware/history` - Returns last N readings
     - POST `/api/export/csv` & `/api/export/json` - Data export

2. **Frontend Templates**
   - ✅ `w.html` - Main dashboard with real-time monitoring
   - ✅ `analytics.html` - Advanced analytics & statistics
   - ✅ `models.html` - ML model performance display
   - ✅ `alerts.html` - Alert management system
   - ✅ `settings.html` - Configuration panel
   - ✅ Admin & Export pages

3. **Hardware Integration**
   - ✅ `test.py` - ESP32 data reader & ML predictor
   - ✅ Data flow: ESP32 → test.py → Flask `/api/hardware/data`
   - ✅ Real-time updates every 5 seconds

4. **Database & Storage**
   - ✅ In-memory hardware_history (500 readings max)
   - ✅ Thread-safe data access with locks
   - ✅ Alerts history (1000 max)

## 🚀 HOW TO START

### 1. Start Flask Server
```bash
cd c:\Users\Balaji Tex\OneDrive\Documents\a
python app.py
```
Server runs on: `http://localhost:5000`

### 2. Login to Dashboard
- URL: `http://localhost:5000/`
- **Demo Credentials:**
  - Admin: `admin` / `admin123`
  - User: `user` / `user123`

### 3. Start Hardware Integration (Optional)
```bash
python test.py
```
- Reads from ESP32 at `192.168.137.36`
- Sends data to Flask every 2 seconds
- Runs ML predictions automatically

## 📊 DASHBOARD FEATURES

### Main Dashboard (`/`)
- Real-time KPI cards (Voltage, Current, Frequency, Health)
- Live Apex Charts (4 synchronized charts)
- Connection Status indicator
- Fault Alerts with recommendations
- Live Data Table

### Analytics Page (`/analytics`)
- Average/Min/Max statistics
- Voltage & Current distribution histograms
- Fault occurrence bar chart
- Hourly trend analysis

### Models Page (`/models`)
- Best model showcase with accuracy
- All 6 models comparison:
  - KNN
  - SVM
  - Random Forest
  - XGBoost
  - LSTM
  - 1D-CNN

### Alerts Page (`/alerts`)
- Critical/Warning/Info categorization
- Active/Resolved status
- Filter buttons
- Real-time alert updates

### Settings Page (`/settings`)
- System configuration
- Alert preferences (alerts, notifications, email)
- Safety thresholds
- Display preferences (theme, animations)

### Admin Panel (`/admin`)
- System statistics
- User management
- Database overview

### Data Export (`/export`)
- CSV format download
- JSON format download
- Full history export

## 🔌 ESP32 HARDWARE INTEGRATION

### How It Works
1. **ESP32** provides live readings at `192.168.137.36`
2. **test.py** reads from `/status` endpoint
3. **test.py** runs ML prediction
4. **test.py** posts JSON to Flask `/api/hardware/data`
5. **Dashboard** fetches data every 5 seconds

### Fault Types Monitored
- SHORT_CIRCUIT_FAULT
- HIGH_VOLTAGE_FAULT
- OPEN_VOLTAGE_FAULT
- FREQUENCY_FAULT
- NORMAL (healthy)

### Data Format
```json
{
  "voltage": 230.5,
  "current": 15.2,
  "frequency": 50.0,
  "fault": "NORMAL"
}
```

## 📁 FILE STRUCTURE

```
c:\Users\Balaji Tex\OneDrive\Documents\a\
├── app.py                          # Flask backend
├── test.py                         # Hardware reader
├── model_results.json              # ML model accuracy data
├── grid_fault_dataset.csv          # Training data
├── templates/
│   ├── w.html                      # Main dashboard
│   ├── analytics.html              # Analytics page
│   ├── models.html                 # Models page
│   ├── alerts.html                 # Alerts page
│   ├── settings.html               # Settings page
│   ├── login.html                  # Login page
│   ├── admin.html                  # Admin panel
│   ├── export.html                 # Export page
│   ├── 404.html                    # Error page
│   └── 500.html                    # Error page
├── static/                         # Static assets (if needed)
├── dec-eb/dec/dec.ino              # ESP32 firmware
└── quick_test.py                   # Endpoint tester

```

## 🔐 Authentication

**Demo Users:**
- `admin` / `admin123` - Full access
- `user` / `user123` - View-only access

**Session Management:**
- Login creates Flask session
- Session required for all dashboard pages
- Unauthenticated requests redirect to `/login`
- API endpoints protected with session validation
- Logout clears session

## 📊 API ENDPOINTS

### Public Endpoints (No Auth)
- `POST /api/hardware/data` - Receive sensor readings

### Protected Endpoints (Require Login)
- `GET /` - Main dashboard
- `GET /live-data` - Current readings
- `GET /api/analytics` - Analytics data
- `GET /api/alerts` - Alert list
- `GET /api/hardware/history` - Reading history
- `GET /api/export/csv` - CSV export
- `GET /api/export/json` - JSON export
- `GET /admin` - Admin panel
- `GET /api/admin/stats` - Admin statistics

## 🧪 TESTING ENDPOINTS

Run the test script:
```bash
python quick_test.py
```

Expected results:
- `/api/hardware/data` POST → Status 200 (JSON response)
- `/api/analytics` GET → Status 200 (valid analytics JSON when logged in)
- `/api/alerts` GET → Status 200 (valid alerts JSON when logged in)
- `/` GET → Redirects to login or shows dashboard

## ⚙️ CONFIGURATION

### Change Flask Port
Edit `app.py` line: `app.run(host="0.0.0.0", port=5000, debug=True)`

### Change Hardware IP
Edit `test.py` line: `ESP_IP = "192.168.137.36"`

### Add More Demo Users
Edit `app.py` USERS dictionary:
```python
USERS = {
    "admin": generate_password_hash("admin123"),
    "newuser": generate_password_hash("password123")
}
```

### Adjust Data History Size
Edit `app.py`:
```python
hardware_history = deque(maxlen=500)  # Change 500 to desired size
```

## 🐛 TROUBLESHOOTING

### Flask won't start
- Check port 5000 is available: `netstat -ano | findstr :5000`
- Verify Python and Flask installed: `python -m flask --version`

### Hardware data not appearing
- Verify ESP32 is running and accessible: `ping 192.168.137.36`
- Check test.py is running: `python test.py`
- Look for errors in Flask console output

### Login not working
- Verify username/password case-sensitive
- Check browser cookies enabled
- Clear browser cache and try again

### Charts not displaying data
- Ensure hardware data is being sent (check `/live-data` API)
- Wait 5-10 seconds for initial data load
- Check browser console for JavaScript errors (F12)

## 📈 CURRENT DATA

- **Stored Readings:** Last 500 hardware readings
- **Chart History:** Last 30 readings displayed
- **Alert History:** Last 50 alerts retained
- **Update Interval:** Every 5 seconds

## 🎯 NEXT STEPS (OPTIONAL ENHANCEMENTS)

1. **Database Integration** - Replace in-memory storage with SQLite/PostgreSQL
2. **Email Alerts** - Implement SMTP for email notifications
3. **Mobile App** - Create mobile dashboard
4. **Data Visualization** - Add more chart types
5. **Multi-user Roles** - Implement admin/technician/viewer roles
6. **Real-time Websockets** - Replace HTTP polling with WebSocket
7. **SSL/TLS** - Add HTTPS for production
8. **Load Testing** - Stress test with 1000+ readings/sec

## 📞 SUPPORT

For issues or questions:
1. Check the troubleshooting section above
2. Review Flask error messages in console
3. Check browser console (F12) for JavaScript errors
4. Verify all files are present in correct locations

---
**Dashboard Version:** 1.0  
**Last Updated:** 2026-03-17  
**Status:** ✅ READY FOR USE
