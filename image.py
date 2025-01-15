from fastapi import FastAPI,Response
# from fastapi.responses import FileResponse
import os
from typing import List, Optional
import pandas as pd
from pydantic import BaseModel
import matplotlib.pyplot as plt
import tempfile
app = FastAPI()

# Create a directory to store the plot images
plot_dir = "plot"
if not os.path.exists(plot_dir):
    os.makedirs(plot_dir)
class RepeatedMeasuresAnovaInput(BaseModel):
    value_column: List[int]
    group_column: Optional[List[object]]=None
    time_column: List[object]
    subject_column: Optional[List[int]] = None


@app.post("/line_plot")
async def get_line_plot(input_data: RepeatedMeasuresAnovaInput):
    """
    Generate a line plot from the input data
    """
    df = pd.DataFrame({
        'value': input_data.value_column,
        'time': input_data.time_column,
    })

    # Generate the plot
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [4, 5, 6])
    # Create a temporary file to store the plot image
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        plot_path = tmp.name
        plt.savefig(plot_path)
    # Return the image file
    baseUrl="https://fastapi-image-test.onrender.com"
    return {"url": baseUrl+f"/plot/{os.path.basename(plot_path)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)
