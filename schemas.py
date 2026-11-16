from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    name: str
    qty_sent: int = Field(default=0, ge=0)
    qty_received: int = Field(default=0, ge=0)
    qty_damaged: int = Field(default=0, ge=0)


class ShipmentCreate(BaseModel):
    qty_sent: int = Field(..., gt=0)
    qty_received: int = Field(default=0, ge=0)
    qty_damaged: int = Field(default=0, ge=0)
