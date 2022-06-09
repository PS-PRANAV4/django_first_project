from xml.dom.minidom import Element
import pyodide
from pyodide.http import pyfetch
import json
from js import document

# def on_click(e):
#     ul = document.getElementById('left')
#     ul.innerHTML = 'hello world'

x=0

async def make_request(url,method,body=None,headers=None):
    default_headers = {
        'X-Requested-with': 'XMLHttpRequest',
        'content-type': 'application/json',

    }

    if  headers:
        headers = default_headers.update(headers)
    response = await pyfetch(
        url=url, method=method, body=body, headers=default_headers
    )

    return await response.json()



# async def get_number_onclick(e):
#     data =await make_request(url='/hello', method='GET')
#     ul = document.getElementById('left')
#     ul.innerHTML = data['number']

async def send_minus_onclick(e):
    
    id = e.target.innerHTML
    csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value
    number = document.getElementById('lome').value;
    body = json.dumps({'number': number})
    headers = {'X-CSRFToken' : csrf}
    data = await make_request(url='/hello',method='POST', body=body,headers=headers)
    ul = document.getElementById('me')
    ul.innerHTML = data['data']
    
# async def send_add_onclick(e):
#     number = 5
    
#     csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value
#     body = json.dumps({'number': number})
#     headers = {'X-CSRFToken' : csrf}
#     data = await make_request(url='/hello',method='POST', body=body,headers=headers)
#     ul = document.getElementById('me')
#     ul.innerHTML = data['data']



def main():

    button = document.getElementById('bus')
    # button1 = document.getElementById('bu')
    # button1.addEventListener('click',pyodide.create_proxy(send_add_onclick))
    button.addEventListener('click',pyodide.create_proxy(send_minus_onclick))
    

main()