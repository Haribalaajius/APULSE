# 🔌 Hardware Integration Setup Guide

## Overview
Your dashboard is now connected to **live hardware readings from your ESP32 microcontroller** via `test.py`. No more ThingSpeak - everything runs locally!

---

## 🚀 How It Works

```
ESP32 Hardware
    ↓
test.py (Reads & Predicts)
    ↓
Flask API (/api/hardware/data)
    ↓
Dashboard (Real-time display)
```

---

## ⚙️ Setup Instructions

### **Step 1: Ensure Your Hardware is Connected**
Make sure your ESP32 is running and accessible at:
```
http://192.168.137.36/status
```

Test it manually in your browser to verify it returns data like:
```
Voltage: 220V
Current: 50mA
Frequency: 50Hz
```

### **Step 2: Start Flask Dashboard**
Open terminal and run:
```bash
python app.py
```

Output should show:
```
 * Running on http://0.0.0.0:5000
 * Debug mode: on
```

### **Step 3: Start Hardware Data Collection (test.py)**
Open another terminal and run:
```bash
python test.py
```

Output should show:
```
✅ Loaded: Model + Scaler + Label Encoder
📥 220.00 V | 1000.00 mA | 50.00 Hz
🔎 PREDICTION: NORMAL
📊 Dashboard Updated ✓
☁️ ThingSpeak: HTTP 200
```

### **Step 4: Access Dashboard**
Open your browser:
```
http://localhost:5000
```

Login with:
- **Username:** `admin` or `user`
- **Password:** `admin123` or `user123`

---

## 📊 Data Flow Details

### **What test.py Does (Every 2 seconds)**
1. ✅ Reads voltage, current, frequency from ESP32
2. ✅ Runs ML model prediction to detect faults
3. ✅ Controls relay (sends fault/normal command)
4. ✅ **Posts data to Flask** (`/api/hardware/data`)
5. ✅ (Optional) Posts to ThingSpeak for cloud backup

### **What Flask Does**
1. ✅ Receives data from test.py
2. ✅ Stores last reading in memory
3. ✅ Maintains history of last 500 readings
4. ✅ Serves data via `/live-data` and `/api/hardware/history`

### **What Dashboard Does**
1. ✅ Fetches current reading every 5 seconds
2. ✅ Fetches last 30 readings for charts
3. ✅ Updates KPI cards in real-time
4. ✅ Shows system status and alerts
5. ✅ Displays connection status

---

## 🎯 Live Data Endpoints

### Current Reading
**Endpoint:** `GET /live-data`
```json
{
  "voltage": 220.5,
  "current": 1050.2,
  "frequency": 50.0,
  "fault": "NORMAL",
  "timestamp": "2024-03-17T10:30:45.123456",
  "status": "CONNECTED"
}
```

### Historical Data
**Endpoint:** `GET /api/hardware/history?limit=100`
```json
{
  "data": [
    {
      "voltage": 220.5,
      "current": 1050.2,
      "frequency": 50.0,
      "fault": "NORMAL",
      "timestamp": "2024-03-17T10:30:45.123456"
    },
    ...
  ],
  "count": 100
}
```

### Send Hardware Data
**Endpoint:** `POST /api/hardware/data`
```json
{
  "voltage": 220.5,
  "current": 1050.2,
  "frequency": 50.0,
  "fault": "NORMAL"
}
```

---

## 🔧 Configuration

### Change Hardware IP (in test.py)
Find line 17:
```python
ESP_IP = "192.168.137.36"
```

### Change Flask Server Address (in test.py)
Find line 23:
```python
FLASK_URL = "http://localhost:5000/api/hardware/data"
```

If running Flask on a different machine:
```python
FLASK_URL = "http://192.168.1.100:5000/api/hardware/data"  # Your machine IP
```

### Change Update Interval (in dashboard w.html)
Find line ~704:
```javascript
setInterval(loadData, 5000);  // 5000 = 5 seconds
```

Change to desired interval:
- `2000` = 2 seconds (more frequent)
- `10000` = 10 seconds (less frequent)

---

## 📊 Dashboard Features with Hardware

### KPI Cards - Show Real-Time Values
- **Voltage** - From ESP32 field1
- **Current** - From ESP32 field2 (scaled)
- **Frequency** - From ESP32 field3
- **System Status** - NORMAL / FAULT prediction

### Charts - Display Historical Data
- **Voltage Trend** - Last 30 readings
- **Current Trend** - Last 30 readings
- **Frequency Trend** - Last 30 readings
- **System Health** - Overall status gauge

### Live Data Table
- Shows last 20 readings
- Updates in real-time
- Timestamp for each reading

### Connection Status
- **Green ✓ Connected** - ESP32 is sending data
- **Red ✗ Disconnected** - No data received in last update

---

## ⚠️ Troubleshooting

### Dashboard Shows "Disconnected"
**Problem:** Flask not receiving data from test.py
**Solutions:**
1. Verify test.py is running
2. Check console output of test.py for errors
3. Check Flask URL in test.py is correct
4. Verify network connectivity

### "ESP ERROR" in test.py
**Problem:** Can't reach ESP32
**Solutions:**
1. Verify ESP32 IP: `ping 192.168.137.36`
2. Check ESP32 is powered on
3. Verify same Wi-Fi network
4. Test endpoint: `http://192.168.137.36/status`

### Data not saving to dashboard
**Problem:** Flask not storing data correctly
**Solutions:**
1. Check Flask console for errors
2. Verify POST request format in test.py
3. Check network firewall isn't blocking
4. Verify Flask is running without errors

### Charts not updating
**Problem:** Dashboard not fetching data
**Solutions:**
1. Open browser console (F12)
2. Check for JavaScript errors
3. Verify `/live-data` endpoint works:
   ```javascript
   fetch('/live-data').then(r => r.json()).then(d => console.log(d))
   ```

---

## 📈 Data Export

### Export CSV
Visit: `http://localhost:5000/export`
- Downloads all hardware readings as CSV
- Includes: Timestamp, Voltage, Current, Frequency, Status

### Export JSON
Visit: `http://localhost:5000/export`
- Downloads structured JSON format
- Includes metadata and full data structure

---

## 🎬 Running Multiple Terminals on Windows

**Option 1: PowerShell (Recommended)**
```powershell
# Terminal 1 - Flask Dashboard
python app.py

# Terminal 2 - Hardware Reader (open new PowerShell)
python test.py
```

**Option 2: Command Prompt**
```cmd
REM Terminal 1
python app.py

REM Terminal 2 (open new CMD)
python test.py
```

**Option 3: Run Asynchronously**
```powershell
# Run in background
Start-Process python -ArgumentList "app.py"
Start-Process python -ArgumentList "test.py"
```

---

## 🔒 Production Deployment

### For Remote Access
1. Change Flask binding:
```python
app.run(host="0.0.0.0", port=5000)  # Accessible from any IP
```

2. Update test.py:
```python
FLASK_URL = "http://your-server-ip:5000/api/hardware/data"
```

3. Use HTTPS (with proper certificates)

---

## 📞 Quick Reference

| Task | Command |
|------|---------|
| Start Dashboard | `python app.py` |
| Start Hardware Reader | `python test.py` |
| Access Dashboard | `http://localhost:5000` |
| Test ESP32 | `http://192.168.137.36/status` |
| Export Data | Visit `/export` page |
| Admin Panel | `http://localhost:5000/admin` |

---

## ✅ Verification Checklist

- [ ] ESP32 is powered and accessible
- [ ] test.py runs without errors
- [ ] Flask app starts successfully
- [ ] Dashboard loads in browser
- [ ] Login works with demo credentials
- [ ] Data updates on KPI cards every 5 seconds
- [ ] Charts show historical data
- [ ] Connection status shows "Connected"
- [ ] Fault detection works when triggered
- [ ] Can export data as CSV/JSON

---

## 🎉 You're Done!

Your dashboard is now **fully integrated with your hardware**! All readings are coming directly from your ESP32 microcontroller through test.py.

**Live monitoring is active and real-time!** 🚀
