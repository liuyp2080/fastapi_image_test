from fastapi import FastAPI,Response
from fastapi.responses import FileResponse
import os
from typing import List, Optional
import pandas as pd
from pydantic import BaseModel
import matplotlib.pyplot as plt
from fastapi.staticfiles import StaticFiles
app = FastAPI()
if not os.path.exists("images"):
    os.makedirs("images")
app.mount("/images", StaticFiles(directory="images"), name="images")
class RepeatedMeasuresAnovaInput(BaseModel):
    value_column: List[int]
    group_column: Optional[List[object]]=None
    time_column: List[object]
    subject_column: Optional[List[int]] = None


@app.post("/line_plot")
async def generate_line_plot(input_data: RepeatedMeasuresAnovaInput) -> dict:
    """
    Generate a line plot from the input data.
    """
    data_frame = pd.DataFrame({
        "value": input_data.value_column,
        "time": input_data.time_column,
    })

    # Create the plot
    figure, axis = plt.subplots()
    axis.plot(data_frame["time"], data_frame["value"])

    # Save the plot to a temporary file
    image_path = "images/plot.png"
    plt.savefig(image_path)

    # Return the URL to access the image
    base_url = "https://fastapi-image-test.onrender.com"
    return {"url": f"{base_url}/images/plot.png"}

@app.get("/images/plot.png")
def get_image():
    """Return the line plot image generated by the POST /line_plot endpoint"""
    image_path = "images/plot.png"
    return FileResponse(image_path, media_type="image/png")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)
