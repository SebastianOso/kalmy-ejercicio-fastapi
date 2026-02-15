from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

class Item(BaseModel):
    """
    Schema para Items un poco general.
    Sirve para crear, actualizar y responder en diferentes casos.
    Cuenta con campos opcionales para crear y actualizar
    """

    id: Optional[int] = None
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="Nombre del item")
    description: Optional[str] = Field(None, min_length=1, max_length=100, description="Descripcion del item")
    price: Optional[float] = Field(None, gt=0, description="Precio del item, debe ser mayor a 0")
    available: Optional[bool] = True
    created_at: Optional[datetime] = None
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
