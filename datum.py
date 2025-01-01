from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi.middleware.cors import CORSMiddleware
import datetime

app = FastAPI()

# Adding CORS middleware configuration to allow requests from any origin.
origins = [
    "*",  # Allow all origins for testing purposes. In production, specify the exact domains you trust.
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


DATABASE_URL = "sqlite:///data.db"
engine = create_engine(DATABASE_URL)

Base = declarative_base()

class Datum(Base):
    __tablename__ = "data"

    id = Column(Integer, primary_key=True)
    device_id = Column(String(50), nullable=False)  
    content = Column(String(140), nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

class DatumRequest(BaseModel):
    content: str

@app.post("/data/{device_id}")
async def create_datum(device_id: str, datum_request: DatumRequest):
    if len(datum_request.content) > 140:
        raise HTTPException(status_code=400, detail="Content is too long")

    datum = Datum(device_id=device_id, content=datum_request.content)
    session.add(datum)

    session.commit()

    return {"id": datum.id, "device_id": datum.device_id, "content": datum.content}
    
@app.get("/data/{device_id}")
async def get_set_data(device_id: str,  content: str | None = None):
    if content:
        if len(content) > 140:
        	raise HTTPException(status_code=400, detail="Content is too long")
        datum = Datum(device_id=device_id, content=content)
        session.add(datum)

        session.commit()

        return {"id": datum.id, "device_id": datum.device_id, "content": datum.content}
            
    else:
        data = session.query(Datum).filter_by(device_id=device_id).all()

        if not data:
            return {"message": "no data"}

        return [{"id": d.id, "device_id": d.device_id, "content": d.content} for d in data]

@app.get("/data/{device_id}/last/{n}")
async def get_last_n_data(device_id: str, n: int):
    if n <= 0:
        raise HTTPException(status_code=400, detail="Invalid value of 'n'")

    last_n_data = session.query(Datum).filter_by(device_id=device_id).order_by(Datum.id.desc()).limit(n).all()

    if not last_n_data:
        return {"message": "no data"}

    return [{"id": d.id, "device_id": d.device_id, "content": d.content} for d in reversed(last_n_data)]

@app.get("/data/last/{n}")
async def get_last_n_device_ids(n: int):
    if n <= 0:
        raise HTTPException(status_code=400, detail="Invalid value of 'n'")

    if n == 0:
        data = session.query(Datum).filter_by(device_id=device_id).all()
    else:                
        data = session.query(Datum).order_by(Datum.id.desc()).limit(n).all()

    if not data:
        return {"message": "no data"}

    return [{"device_id": d.device_id} for d in reversed(data)]

@app.get("/devices")
async def get_registered_devices():
    result = session.query(Datum.device_id).distinct().all()
    device_ids = [row[0] for row in result]

    return {"device_ids": device_ids}
        
@app.get("/data/{device_id}/since/{t1}")
async def get_since_t(device_id: str, t1):
    try:
        t1 = datetime.datetime.strptime(t1, "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid timestamp")

    data = session.query(Datum).filter_by(device_id=device_id).filter(Datum.timestamp >= t1).all()

    if not data:
        return {"message": "no data"}

    return [{"id": d.id, "device_id": d.device_id, "content": d.content} for d in data]

@app.get("/data/{device_id}/between/{t1}/{t2}")
async def get_between_t(device_id: str, t1, t2):
    try:
        t1 = datetime.datetime.strptime(t1, "%Y-%m-%dT%H:%M:%S")
        t2 = datetime.datetime.strptime(t2, "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid timestamp")

    data = session.query(Datum).filter_by(device_id=device_id).filter(Datum.timestamp >= t1).filter(Datum.timestamp <= t2).all()

    if not data:
        return {"message": "no data"}

    return [{"id": d.id, "device_id": d.device_id, "content": d.content} for d in data]

@app.get("/data/{device_id}/{datum_id}")
async def get_datum(device_id: str, datum_id: int):
    datum = session.query(Datum).filter_by(device_id=device_id, id=datum_id).first()

    if not datum:
        raise HTTPException(status_code=404, detail="Datum not found")

    return {"id": datum.id, "device_id": datum.device_id, "content": datum.content}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
