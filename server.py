import os
import shutil
import uuid
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from main import predict  # We reuse the logic from your main.py

app = FastAPI(title="Industrial Acoustic Anomaly Detection API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def health_check():
    return {"status": "online", "message": "MIMII Anomaly Detection Server is running"}

@app.post("/analyze")
async def analyze_audio(
    machine_type: str = Form(...), 
    file: UploadFile = File(...)
):
    # 1. Normalize Input (Avoids "string not supported" errors)
    m_type = machine_type.lower().strip()
    
    if m_type not in ["fan", "pump", "valve", "slider"]:
        raise HTTPException(status_code=400, detail=f"Unsupported machine type: {m_type}")

    file_id = str(uuid.uuid4())
    temp_path = os.path.join(UPLOAD_DIR, f"{file_id}_{file.filename}")
    
    try:
        # Save temp file
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # 2. Run Inference
        anomaly_score, raw_mse, visual_b64 = predict(temp_path, m_type)
        
        # 3. Calibrated Threshold Logic (BASED ON YOUR SPECIFIC MODEL OUTPUTS)
        # Normal Slider was -1.22, so we set threshold slightly higher at -1.0
        thresholds = {
            "fan": -3.2,
            "pump": -3.5,
            "valve": -2.8,
            "slider": -2.1
        }
        
        thresh = thresholds.get(m_type, -2.0)
        is_anomaly = anomaly_score > thresh

        # 4. Confidence Heuristic (Scaled to 100%)
        # Measures how far the score is from the threshold
        diff = abs(anomaly_score - thresh)
        confidence = min(100.0, round(diff * 25, 2)) 

        # 5. Diagnostic logging (Helps you debug in the terminal)
        print(f"--- [AI LOG] Machine: {m_type} | Score: {anomaly_score} | Threshold: {thresh} ---")

        return {
            "filename": file.filename,
            "machine_type": m_type,
            "results": {
                "anomaly_score": round(float(anomaly_score), 4),
                "threshold": thresh,
                "is_anomaly": bool(is_anomaly),
                "confidence": confidence,
                "severity": "Critical" if is_anomaly and diff > 0.5 else "Warning" if is_anomaly else "Normal"
            },
            "visualization": f"data:image/png;base64,{visual_b64}",
            "status": "success"
        }

    except Exception as e:
        print(f"--- [SERVER ERROR] {str(e)} ---")
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)