from fastapi import FastAPI, UploadFile
import shutil
from parser import parse_resume
from ai_matcher import match_with_jd

app = FastAPI()


@app.post("/upload_resume")
async def upload(file: UploadFile):

    path = f"temp_{file.filename}"

    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = parse_resume(path)

    return {"message": "resume uploaded", "resume": text}



@app.post("/match")
async def match(data: dict):

    resume_text = data.get("resume","")
    jd = data.get("jd","")

    if not resume_text or not jd:
        return {"error":"empty input"}

    result = match_with_jd(resume_text, jd)

    return result
