from fastapi import FastAPI, Query
from typing import Annotated

app = FastAPI()

# You could also define it as a normal function instead of async def:
@app.get("/")
async def root():
    return {"message":"Hello Word FastAPI"}

@app.get("/items/{items_id}")
def get_items(items_id: int):
    return {"data":f"items id:{items_id}"}

# parms
@app.get("/get_parmas/")
def get_parmas(name: str, age: int | None=None, married: bool=False):
    data = {
        "name":name,
        "age":age,
        "married":married
    }
    return data



# Request body
from pydantic import BaseModel

class ItemModel(BaseModel):
    name: str
    desc: str | None = None
    price: float
    tax: float | None = None


# @app.post("/create_item")
# async def create_item(item:ItemModel):
#     return item

# Inside of the function, you can access all the attributes of the model object directly:


@app.post("/create_item")
async def create_item(item:ItemModel):
    item_dic = item.model_dump()
    if item.tax is not None:
        price_with_tax = item.price+item.tax
        item_dic.update({"price_with_tax":price_with_tax})

    return item_dic


# Request body + path parameters
# You can declare path parameters and request body at the same time.


@app.put("/update_item/{item_id}")
async def update_items(item_id:int,item:ItemModel):
    return {"item id":item_id,**item.model_dump()}

# Request body + path + query parameters¶
# You can also declare body, path and query parameters, all at the same time.

@app.put("/update_items_parms/{item_id}")
async def update_items_parms(item_id:int, item:ItemModel, query: str | None = None):
    result = {"item_id":item_id,**item.model_dump()}
    if query:
        result.update({"query_params":query})
    
    return result


# Query Parameters and String Validations
# 1
# simple
# @app.get("/query_data")
# async def query_data(q: str | None = None):
#     results = {"data":[{"id":1,"name":"Ali"},{"id":2,"name":"Ahmed"}]}
#     if q:
#         results.update({"q_data":q})
#     return results

# proper json return under data key
# self
# @app.get("/query_data")
# async def query_data(q: str | None = None):
#     results = [{"id":1,"name":"Ali"},{"id":2,"name":"Ahmed"}]
#     if q:
#         results.append({"q_data":q})
#     return {"data":results}

# add validation max char length for querying
# we need import query from fastapi and annotate from typing
# @app.get("/query_data")
# async def query_data_max_val(q: Annotated[str | None, Query(max_length=20)] = None ):
#     results = {"data":[{"id":1,"name":"Ali"},{"id":2,"name":"Ahmed"}]}
#     if q:
#         results.update({"query_data":q})
#     return results

# asu a lrean like we use as optional like None = None but we can give default value eg below
# Annotated[str | None, Query(max_length=20)] = "defaultquery data"

# Add more validations¶

# 3 here we learn minx and max
# min length 
# fixedquery pattern="^fixedquery$
# fixedquery use hardcored parms its use in a suppose user deleting data so(cont)
# so when he delete if he pas fixedquery mean (YES_I_UNDERSTAND) so we allow to delete
# With ^fixedquery$ → strict exact match
# With fixedquery only → substring match allowed eg
# fixedquery123, 123fixedquery its a ccept these also if we dont use regix

# @app.get("/query_data")
# async def query_data_max_val(q: Annotated[str | None, Query(min_length=3,max_length=13,pattern="^fixedquery$")] = None ):
#     results = {"data":[{"id":1,"name":"Ali"},{"id":2,"name":"Ahmed"}]}
#     if q:
#         results.update({"query_data":q})
#     return results


# Last topic I was reading → “Add Regular Expressions (pattern validation in FastAPI Query)”

# Last topic 
# Add regular expressions
# https://fastapi.tiangolo.com/tutorial/query-params-str-validations/#add-more-validations

# 25 dec

# 1
# we can pass default value for parameter
# @app.get("/query_data")
# async def query_data_max_val(q: Annotated[str | None, Query(min_length=3,max_length=23)] = "default value" ):
#     results = {"data":[{"id":1,"name":"Ali"},{"id":2,"name":"Ahmed"}]}
#     if q:
#         results.update({"query_data":q})
#     return results


# 2
# Query parameter list / multiple values
# @app.get("/multi_query")
# async def multi_query(q: Annotated[list[str]| None, Query()]= None):
#     query_items = {"q":q}
#     return query_items

# 3
# Query parameter list / multiple values with defaults¶
# @app.get("/multi_query")
# async def multi_query(q: Annotated[list[str]| None, Query()]=["foo", "bar"]):
#     query_items = {"q":q}
#     return query_items

"""
Today Topic
Using just list
"""
# Using just list¶
# You can also use list directly instead of list[str]:

"""
Notes
For example, list[int] would check (and document) that the contents of the list are integers. But list alone wouldn't.


"""

# 1
# You can also use list directly instead of list[str]:

# @app.get('/item_list')
# async def query_as_list(q: Annotated[list[str], Query()]=[]):
#     query_list = {"q":q}
#     return query_list

# 
# ---2
# Declare more metadata¶
# You can add more information about the parameter.

# That information will be included in the generated OpenAPI and used by the documentation user interfaces and external tools.

# @app.get('/item_list')
# async def query_as_list(q: Annotated[list[str], Query(title="testing title",description="More text as description")]=[]):
#     query_list = {"q":q}
#     return query_list


"""
Topic of the start of the day 
Alias parameters

Alias parameters¶
Imagine that you want the parameter to be item-query.

Like in:


http://127.0.0.1:8000/items/?item-query=foobaritems
But item-query is not a valid Python variable name.

The closest would be item_query.

But you still need it to be exactly item-query...

Then you can declare an alias, and that alias is what will be used to find the parameter value:



"""

########
# -1-   #
########

# @app.get("/alias_parms")
# async def use_alias_params(q: Annotated[str | None, Query(alias="query-items")] = None):
#     alias_data = {"alias":"temp data val"}
#     if q:
#         alias_data.update({"data":q})
    
#     return alias_data
# we use here http://127.0.0.1:8000/alias_parms/?query-items=fixedqueryy instead of query parmas


########
# -2-   #
########
# Deprecating parameters
# meaning Deprecated = Allowed for now, but discouraged + will probably be removed later.
# Simple example:

# Old endpoint: /v1/users → Deprecated

# New endpoint: /v2/users → Use this instead
# The docs will show it like this:deprecate in docs in red



# @app.get("/see_dep")
# async def see_dep_doc(
#     q: Annotated[
#         str | None, Query(
#             title="Title for deprecating params",
#             description= "Allowed for now, but discouraged + will probably be removed later.",
#             min_length=3,
#             max_length=10,
#             deprecated=True  #make Deprecated true 
#         )
#     ]
# ):
#     data = {"key":"value"}
#     if q:
#         data.update({"query":q})
#     return data




#-----------------------#
# -3-   #
#-----------------------#
# Exclude parameters from OpenAPI
# if we make include_in_schema false so in api documention their No parameters



# @app.get("/see_exclude_params")
# async def get_exclude_params(q: Annotated[str | None, Query(include_in_schema=False)] = None):
#     default_data = {"key":"default data value"}
#     if q:
#         default_data.update({"add data":q})
#     return default_data



"""
Custom Validation
There could be cases where you need to do some custom validation that can't be done with the parameters shown above.

In those cases, you can use a custom validator function that is applied after the normal validation (e.g. after validating that the value is a str).

You can achieve that using Pydantic's AfterValidator inside of Annotated.
"""
from pydantic import AfterValidator
import random

data = {
    "isbn-9781529046137": "The Hitchhiker's Guide to the Galaxy",
    "imdb-tt0371724": "The Hitchhiker's Guide to the Galaxy",
    "isbn-9781439512982": "Isaac Asimov: The Complete Stories, Vol. 2",
}

#-----------------------#
# -1-   #
#-----------------------#

def check_validation_id(id:str):
    if not id.startswith(("isbn-","imdb-")):
        raise ValueError('Invalid ID format, it must start with "isbn-" or "imdb-"')
    return id


@app.get('/custom_validation')
async def get_custom(id: Annotated[str | None, AfterValidator(check_validation_id)]=None):
    if id:
        item = data.get(id)

    else:
        id, item = random.choice(list(data.items()))

    
    return {"id":id,"item":item}





"""
Next day topic Custom Validation (Understand that Code and recap)
https://fastapi.tiangolo.com/tutorial/query-params-str-validations/#custom-validation
"""





