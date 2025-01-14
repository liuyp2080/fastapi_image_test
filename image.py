from fastapi import FastAPI
from fastapi.responses import FileResponse
import os
from typing import List, Optional
import pandas as pd
from pydantic import BaseModel

import matplotlib.pyplot as plt
app = FastAPI()
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
    plot = df.plot(x='time', y='value', kind='line', title='Line Plot', figsize=(10, 6))

   # Save the plot to a temporary file
    img_path = 'temp.png'
    plt.savefig(img_path)

    # Return the image file
    return FileResponse(img_path, media_type='image/png')

    # Don't forget to delete the temporary file
    os.remove(img_path)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)
