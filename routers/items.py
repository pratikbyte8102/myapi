from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from database import get_session
from models import Item, ItemCreate, ItemRead, User
from auth import get_current_user

router = APIRouter(prefix="/items", tags=["Items"])

@router.post("", response_model=ItemRead)
def create_item(item: ItemCreate, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    db_item = Item(**item.model_dump(), owner_id=current_user.id)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item


@router.get("", response_model=list[ItemRead])
def get_all_items(session: Session = Depends(get_session)):
    return session.exec(select(Item)).all()


@router.get("/{item_id}", response_model=ItemRead)
def get_item(item_id: int, session: Session = Depends(get_session)):
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.put("/{item_id}", response_model=ItemRead)
def update_item(item_id: int, updated_item: ItemCreate, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if item.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to edit this item")

    item.name = updated_item.name
    item.price = updated_item.price
    item.in_stock = updated_item.in_stock
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@router.delete("/{item_id}")
def delete_item(item_id: int, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if item.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this item")

    session.delete(item)
    session.commit()
    return {"message": "Item deleted"}


@router.get("/me/my-items", response_model=list[ItemRead])
def get_my_items(current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    return session.exec(select(Item).where(Item.owner_id == current_user.id)).all()