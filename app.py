import os
import uuid
import pandas as pd

from fastapi import FastAPI,UploadFile,File
from fastapi.responses import FileResponse

from src.pipeline.inference import run_full_pipeline

#CORS- Cross origin resource sharing --This creates a middleware
#middleware--piece of software in between user and UI
#Controls which website or application are allowed to communicate with
#our FASTAPI application,we do not expose it to all the softwares
#uber services can not be used by zomato
#adds enhances security to our application

from fastapi.middleware.cors import CORSMiddleware
os.makedirs("data",exist_ok=True)

#we need not create a UI(frontend logic) ..it is created by fastAPI 
#this ui is called as swagger UI which is internally supported by fastAPI 
#this is useful for testing purpose
#Fast API service is you test UI by yourself before giving to frontend developer
app = FastAPI(
    title = "Customer Support QA Evaluation",
    version = "1.0"
)

#give value,which software,header is allowed to access
#here we have given * which includes all origins (flexible for all)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],


)
#decorator which adds a feature to health_check()
#When we hit this route(function),we need tp get some information
# "/" is default can also be "/health"
@app.get("/health")
def health_check():
    return {"message" : "QA Evaluator API is running"}

#this method expects a file arg
#UploadFile and File are imported from FastAPI
#this is to post upload input to the user
@app.post("/evaluate-file")
async def evaluate_file(file: UploadFile = File(...)):
    allowed_extensions = [".csv",".xlsx"]

    #This would split the file name and we get the extension in [1]
    file_extension = os.path.splitext(file.filename)[1].lower()

    if file_extension not in allowed_extensions:
        return {"error" : "Please upload a csv or xlsx file"}

    #Create temporary paths
    #uuid creates a unique id , which is added before the file name when the file is saved
    #unique id is created with datetime stamp
    input_path = f"data/{uuid.uuid4()}{file_extension}"
    output_path = f"data/output_{uuid.uuid4()}.xlsx"

    # why WB? we get data from the llm and add as column 
    # why await? make this func as async and user2 need not wait when user1 works and await helps not to remain blocked
    with open(input_path,"wb") as f:
        content = await file.read()
        f.write(content)

    #loading the files dynamically

    if file_extension == ".csv":
        df = pd.read_csv(input_path)

    elif file_extension == ".xlsx":
        df = pd.read_excel(input_path)

    output_df = run_full_pipeline(df)
    output_df.to_excel(output_path,index=False)

    # we need to return the file (output) to the user 
    #In the frontend we give an option for the user to download the file
    #media_type value can be taken from the fastapi documentation
    return FileResponse(
        path = output_path,
        filename = "qa_output.xlsx",
        media_type= "application/vnd.openxmlformats-officedocument.spreadsheetm1.sheet"
    )

