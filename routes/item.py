from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
import math
from config.db import get_db
from models.item import Item as ItemModel
from schemas.item import Item as ItemSchema

router = APIRouter(
    prefix="/items",
    tags=["items"]
)

@router.get("/{item_id}", response_model=ItemSchema)
def obtener_item(item_id: int, db: Session = Depends(get_db)):
    """
    Obtiene un item individual dependiendo del ID
    """

    item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
    
    # 
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item con ID {item_id} no encontrado"
        )
    
    return item