import uvicorn
from typing import Union
from var_dump import var_dump
from php_var_dump import php_var_dump
from fastapi import FastAPI, Form, HTTPException
from typing import Optional, List
from sqlmodel import Field, Session, SQLModel, create_engine
from model import Item, Coord, CoordOut, Hero, Todo

app = FastAPI(title="TODO API", version="V1")


@app.get("/")
async def read_root():
    var_dump({"Hello": "World"})
    return {"Hello": "World"}


@app.get("/component/{component}")
async def component_get(component: int):
    return {"component": component}


@app.get("/component/")
async def component_read(number: int, text: str, name: Optional[str]):
    return {"number": number, "text": text, "name": name}


# @app.post("/position/{priority}")
# async def position(priority: int, coord: Coord, value: bool):
#     return {"priority": priority, "new_coord": coord.dict(), "value": value}

@app.post("/position", response_model=CoordOut)
async def position(coord: Coord):
    return coord.dict()
    # return {"new_coord": coord.dict()}
    #

@app.post("/hero")
async def hero_create(hero: Hero):
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
    hero_2 = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
    hero_3 = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48)

    # engine = create_engine("mysql+mysqlconnector://root@localhost:3306/fastap")
    # SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
    engine = create_engine("sqlite:///database.db")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        session.add(hero_1)
        session.add(hero_2)
        session.add(hero_3)
        session.commit()
    return "OKKKK"
    # return {"new_coord": coord.dict()}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}


# TODOS APPLICATION CRUD
store_todos = []

@app.get("/todos", response_model=List[Todo])
async def todos_all():
    var_dump(store_todos)
    return store_todos


@app.get("/todos/{id}", response_model=Todo)
async def todos_one(id: int):
    try:
        return store_todos[id]
    except:
        raise HTTPException(status_code=404, detail="Todo Not Found in database")


@app.post("/todos")
async def todos_create(todo: Todo):
    try:
        store_todos.append(todo)
        return todo
    except:
        raise HTTPException(status_code=404, detail="Impossible To Add Todo")


@app.put ("/todos/{id}")
async def todos_update(id: int, newtodo: Todo):
    try:
        store_todos[id] = newtodo
        return newtodo
    except:
        raise HTTPException(status_code=404, detail="Todo Not Found in database")


@app.delete("/todos/{id}")
async def todos_delete(id: int):
    try:
        obj = store_todos[id]
        store_todos.pop(id)
        return obj
    except:
        raise HTTPException(status_code=404, detail="Todo Not Found in database")


##
@app.post("/login/")
async def user_login(todo: Todo):
    try:
        store_todos.append(todo)
        return todo
    except:
        raise HTTPException(status_code=404, detail="Impossible To Add Todo")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8181)

