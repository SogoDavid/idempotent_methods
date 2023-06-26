from fastapi import APIRouter
from fastapi import FastAPI
from pydantic import BaseModel

class ChangeBalance(BaseModel):
    balance: int


app = FastAPI()
balance = 0

router = APIRouter(prefix="/balance", tags=["Balance"])

@router.get("")
async def get_balance():
    return balance


@router.patch("/add_balance")
async def add_balance(change_balance: ChangeBalance):
    global balance
    balance += change_balance.balance
    return balance

@router.patch("/sub_balance")
async def sub_balance(change_balance: ChangeBalance):
    global balance
    balance -= change_balance.balance
    return balance

@router.patch("/idempotent/update_balance")
async def sub_balance(change_balance: ChangeBalance):
    global balance
    balance = change_balance.balance
    return balance


@router.put("/update_balance")
async def update_balance(change_balance: ChangeBalance):
    global balance
    balance = change_balance.balance
    return balance

wrong_router = APIRouter(prefix="/wrong_method", tags=["Некорректная реализация методов"])

@wrong_router.get(
    "/add_balance",
    description="GET запрос должен быть идемпотентным и безопасном. "
                "В данном случае он не безопасный и не идемпотентный"
)
async def add_balance(change_balance: int):
    global balance
    balance += change_balance
    return balance

@wrong_router.put(
    "/add_balance",
    description="PUT запрос должен быть идемпотентным."
                "В данном случае он не идемпотентный, т.к. каждый повторный вызов меняет состояние"
)
async def add_balance(change_balance: int):
    global balance
    balance += change_balance
    return balance


app.include_router(router=router)
app.include_router(router=wrong_router)





