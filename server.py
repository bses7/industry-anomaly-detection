import os
import shutil
import uuid
import sqlite3
from datetime import datetime
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from main import predict 

app = FastAPI(title="Industrial Acoustic Anomaly Detection API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
DB_PATH = "history.db"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scan_history (
            id TEXT PRIMARY KEY,
            filename TEXT,
            machine_type TEXT,
            anomaly_score REAL,
            is_anomaly INTEGER,
            severity TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def save_to_history(data):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO scan_history (id, filename, machine_type, anomaly_score, is_anomaly, severity, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        str(uuid.uuid4()),
        data["filename"],
        data["machine_type"],
        data["results"]["anomaly_score"],
        1 if data["results"]["is_anomaly"] else 0,
        data["results"]["severity"],
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))
    conn.commit()
    conn.close()

@app.get("/")
def health_check():
    return {"status": "online", "message": "MIMII Anomaly Detection Server is running"}

@app.get("/history")
async def get_history():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row # Allows access by column name
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM scan_history ORDER BY timestamp DESC LIMIT 20')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.post("/analyze")
async def analyze_audio(
    machine_type: str = Form(...), 
    file: UploadFile = File(...)
):
    m_type = machine_type.lower().strip()
    if m_type not in ["fan", "pump", "valve", "slider"]:
        raise HTTPException(status_code=400, detail=f"Unsupported machine type: {m_type}")

    file_id = str(uuid.uuid4())
    temp_path = os.path.join(UPLOAD_DIR, f"{file_id}_{file.filename}")
    
    try:
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        anomaly_score, raw_mse, visual_b64 = predict(temp_path, m_type)
        
        thresholds = {"fan": -3.2, "pump": -3.5, "valve": -2.8, "slider": -2.1}
        thresh = thresholds.get(m_type, -2.0)
        is_anomaly = anomaly_score > thresh
        diff = abs(anomaly_score - thresh)
        
        # Create the timestamp here
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        response_data = {
            "filename": file.filename,
            "machine_type": m_type,
            "timestamp": now,  # <--- ADD THIS LINE
            "results": {
                "anomaly_score": round(float(anomaly_score), 4),
                "threshold": thresh,
                "is_anomaly": bool(is_anomaly),
                "confidence": min(100.0, round(diff * 25, 2)),
                "severity": "Critical" if is_anomaly and diff > 0.5 else "Warning" if is_anomaly else "Normal"
            },
            "visualization": f"data:image/png;base64,{visual_b64}",
            "status": "success"
        }

        save_to_history(response_data)
        return response_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)