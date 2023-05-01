from io import BytesIO
from typing import List

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse, JSONResponse

from model import load_model, predict, prepare_image
from PIL import Image
from pydantic import BaseModel
from core.config import settings
import base64


templates = Jinja2Templates(directory="templates")
predict_router = APIRouter()
model = load_model()

# Define the response JSON
class Prediction(BaseModel):
    filename: str
    content_type: str
    predictions: List[dict] = []

@predict_router.get("/predict")
async def home(request: Request):
	return templates.TemplateResponse("general_pages/predict_ima.html",{"request":request})

@predict_router.post("/predict", response_model=Prediction)
async def prediction(request: Request, file: UploadFile = File(...)):

    # Ensure that the file is an image
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File provided is not an image.")

    content = await file.read()
    image = Image.open(BytesIO(content)).convert("RGB")
    base64_encoded_image = base64.b64encode(content).decode("utf-8")

    # preprocess the image and prepare it for classification
    image = prepare_image(image, target=(224, 224))

    response = predict(image, model)

    # return the response as a JSON
    #return {
    #    "filename": file.filename,
    #    "content_type": file.content_type,
    #    "predictions": response,
    #}
    print(response)
    context = {
        "request": request,
        "result": max(response, key=lambda x: x['score'])['class'],
        "myImage": base64_encoded_image
    }
    return templates.TemplateResponse("general_pages/predict_ima.html",context)