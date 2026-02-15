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

@router.post("/", response_model=ItemSchema, status_code=status.HTTP_201_CREATED)
def crear_item(item: ItemSchema, db: Session = Depends(get_db)):
    """
    Crear un nuevo item
    """
    
    #Validar que todos los campos esten en la request
    if not item.name or not item.description or item.price is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="name, description y price son requeridos"
        )
    
    nuevo_item = ItemModel(
        name = item.name,
        description= item.description,
        price = item.price,
        available = item.available if item is not None else True
    )

    db.add(nuevo_item)
    db.commit()
    db.refresh(nuevo_item)
    return nuevo_item


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