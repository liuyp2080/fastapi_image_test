from fastapi import FastAPI, Response
from PIL import Image
import io
from typing import List, Optional
import pandas as pd
from pydantic import BaseModel

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

    # Convert the plot to a PNG image
    img_buffer = io.BytesIO()
    plot.figure.savefig(img_buffer, format='png')

    # Return the image as a response
    img_buffer.seek(0)
    return Response(content=img_buffer.getvalue(), media_type='image/png')
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)
