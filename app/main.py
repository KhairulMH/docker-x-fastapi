from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, validator
import joblib
import numpy as np

# Load the model
model = joblib.load('app/car_insurance_fraud_model.joblib')

app = FastAPI()

# Define the data model for the input with validation
class InsuranceData(BaseModel):
    AccidentArea: int = Field(..., example=1, description="Area of the accident: 1 for Urban, 0 for Rural")
    AgentType: int = Field(..., example=0, description="Type of agent: 0 for External, 1 for Internal")
    Fault: int = Field(..., example=1, description="Fault of the accident: 0 for Policy holder, 1 for Third party")
    MaritalStatus: int = Field(..., example=2, description="Marital status: 1 for Married, 2 for Single, 0 for Divorced, 3 for Widow")
    PoliceReportFiled: int = Field(..., example=1, description="Whether police report was filed: 0 for No, 1 for Yes")
    Sex: int = Field(..., example=1, description="Gender: 1 for Male, 0 for Female")
    VehicleCategory: int = Field(..., example=1, description="Category of the vehicle: 0 for Sedan, 1 for Sport, 2 for Utility")
    WitnessPresent: int = Field(..., example=1, description="Whether a witness was present: 0 for No, 1 for Yes")

    @validator('AccidentArea')
    def validate_accident_area(cls, value):
        if value not in [0, 1]:
            raise ValueError("AccidentArea must be 0 (Rural) or 1 (Urban)")
        return value

    @validator('AgentType')
    def validate_agent_type(cls, value):
        if value not in [0, 1]:
            raise ValueError("AgentType must be 0 (External) or 1 (Internal)")
        return value

    @validator('Fault')
    def validate_fault(cls, value):
        if value not in [0, 1]:
            raise ValueError("Fault must be 0 (Policy holder) or 1 (Third party)")
        return value

    @validator('MaritalStatus')
    def validate_marital_status(cls, value):
        if value not in [0, 1, 2, 3]:
            raise ValueError("MaritalStatus must be 0 (Divorced), 1 (Married), 2 (Single), or 3 (Widow)")
        return value

    @validator('PoliceReportFiled')
    def validate_police_report_filed(cls, value):
        if value not in [0, 1]:
            raise ValueError("PoliceReportFiled must be 0 (No) or 1 (Yes)")
        return value

    @validator('Sex')
    def validate_sex(cls, value):
        if value not in [0, 1]:
            raise ValueError("Sex must be 0 (Female) or 1 (Male)")
        return value

    @validator('VehicleCategory')
    def validate_vehicle_category(cls, value):
        if value not in [0, 1, 2]:
            raise ValueError("VehicleCategory must be 0 (Sedan), 1 (Sport), or 2 (Utility)")
        return value

    @validator('WitnessPresent')
    def validate_witness_present(cls, value):
        if value not in [0, 1]:
            raise ValueError("WitnessPresent must be 0 (No) or 1 (Yes)")
        return value

# Define the root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Car Insurance Fraud Prediction API"}

@app.post('/vehicle_insurance_fraud(Beta)/predict')
def predict(data: InsuranceData):
    try:
        data = data.dict()
        features = [
            data['AccidentArea'],
            data['AgentType'],
            data['Fault'],
            data['MaritalStatus'],
            data['PoliceReportFiled'],
            data['Sex'],
            data['VehicleCategory'],
            data['WitnessPresent']
        ]
        prediction = model.predict([features])
        prediction_result = int(prediction[0])  # Convert to integer if prediction is an array

        if prediction_result == 0:
            result = "Not Fraud"
        else:
            result = "Fraud"

        return {'prediction': result}
    except Exception as e:
        # Log the error (you might want to log to a file in a real-world application)
        print(f"Error during prediction: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
