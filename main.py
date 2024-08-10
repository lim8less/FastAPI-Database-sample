from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from models import User, Item
from database import get_session
from schemas import UserCreate, UserRead, ItemCreate, ItemRead
from typing import List

app = FastAPI()

# Create a new user
@app.post("/users/", response_model=UserRead)
async def create_user(user: UserCreate, session: AsyncSession = Depends(get_session)):
    new_user = User(name=user.name, email=user.email)
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user

# Get a user by ID
@app.get("/users/{user_id}", response_model=UserRead)
async def get_user(user_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User).filter_by(id=user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Update a user by ID
@app.put("/users/{user_id}", response_model=UserRead)
async def update_user(user_id: int, user: UserCreate, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User).filter_by(id=user_id))
    existing_user = result.scalar_one_or_none()
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    query = (
        update(User)
        .where(User.id == user_id)
        .values(name=user.name, email=user.email)
        .execution_options(synchronize_session="fetch")
    )
    await session.execute(query)
    await session.commit()

    result = await session.execute(select(User).filter_by(id=user_id))
    updated_user = result.scalar_one_or_none()
    return updated_user

# Delete a user by ID
@app.delete("/users/{user_id}")
async def delete_user(user_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User).filter_by(id=user_id))
    existing_user = result.scalar_one_or_none()
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    query = delete(User).where(User.id == user_id)
    await session.execute(query)
    await session.commit()
    return {"message": "User deleted successfully"}

# Create a new item
@app.post("/items/", response_model=ItemRead)
async def create_item(item: ItemCreate, session: AsyncSession = Depends(get_session)):
    new_item = Item(title=item.title, description=item.description, owner_id=item.owner_id)
    session.add(new_item)
    await session.commit()
    await session.refresh(new_item)
    return new_item

# Get an item by ID
@app.get("/items/{item_id}", response_model=ItemRead)
async def get_item(item_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Item).filter_by(id=item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

# Update an item by ID
@app.put("/items/{item_id}", response_model=ItemRead)
async def update_item(item_id: int, item: ItemCreate, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Item).filter_by(id=item_id))
    existing_item = result.scalar_one_or_none()
    if not existing_item:
        raise HTTPException(status_code=404, detail="Item not found")

    query = (
        update(Item)
        .where(Item.id == item_id)
        .values(title=item.title, description=item.description)
        .execution_options(synchronize_session="fetch")
    )
    await session.execute(query)
    await session.commit()

    result = await session.execute(select(Item).filter_by(id=item_id))
    updated_item = result.scalar_one_or_none()
    return updated_item

# Delete an item by ID
@app.delete("/items/{item_id}")
async def delete_item(item_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Item).filter_by(id=item_id))
    existing_item = result.scalar_one_or_none()
    if not existing_item:
        raise HTTPException(status_code=404, detail="Item not found")

    query = delete(Item).where(Item.id == item_id)
    await session.execute(query)
    await session.commit()
    return {"message": "Item deleted successfully"}

# Get all items for a user
@app.get("/users/{user_id}/items", response_model=List[ItemRead])
async def get_items_for_user(user_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Item).filter_by(owner_id=user_id))
    items = result.scalars().all()
    if not items:
        raise HTTPException(status_code=404, detail="No items found for this user")
    return items
