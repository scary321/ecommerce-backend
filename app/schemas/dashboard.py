from pydantic import BaseModel, ConfigDict

class DashboardResponse(BaseModel):
    users:int
    products:int
    orders:int
    pending_orders:int
    processing_orders:int
    shipped_orders:int
    delivered_orders:int
    cancelled_orders:int
    sales:float
    
    model_config = ConfigDict(from_attributes=True)