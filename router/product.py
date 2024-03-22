from fastapi import APIRouter, Depends, Header, Cookie, Form
from fastapi.responses import PlainTextResponse, Response
from typing import Optional
import time
from custom_log import log

router = APIRouter(
    prefix="/product",
    tags=["product"],
)

products = ['watch', 'phone', 'laptop']

async def time_consuming_function():
    time.sleep(5)
    return "ok"

@router.post('/new')
def create_product(name:str = Form(...)):
    products.append(name)
    return products

@router.get('/all')
async def get_all_products():
    log("MyAPI", "Call to get all products")
    await time_consuming_function()
    # Return all products
    data = ", ".join(products)
    response = Response(content=data, media_type="text/plain")
    response.set_cookie(key="products_cookie", value="products_cookie_value")
    return response

@router.get('/withheader')
def get_products(response: Response, custom_header: Optional[list[str]] = Header(None), products_cookie: Optional[str] = Cookie(None)):
    if custom_header:
        response.headers["custom_response_header"] = custom_header.__str__()
    return {
        'data': products,
        'custom_header': custom_header,
        'my_cookie': products_cookie
    }


@router.get('/{id}', responses={
    200: {
        "content": {"text/html": {
            "example":"<div>Product</div>"
        }},
        "description": "Return the HTML for an object",
    },
    404: {
        "content": {"text/plain": {
                "example":"Product not available"
            }},
        "description": "A clearertext error message",
    }
})
def get_product(id: int):

    if id>=len(products):
        out = "Product not available"
        return PlainTextResponse(status_code=404, content=out, media_type="text/plain")
    else:
        product = products[id]
        out = f"""
        <head>
            <style>
            .product {{
                width: 500px;
                height: 30px;
                border: 2px inset green;
                background-color: lightblue;
                text-align : center;
            }}
            </style>
        </head>
        <body>
            <div class="product">
                <h2>Product Name: {product}</h2>
            </div>
        </body>
        """
        return Response(content=out, media_type="text/html")