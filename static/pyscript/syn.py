from xml.dom.minidom import Element
import pyodide
from pyodide.http import pyfetch
import json
from js import document




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


async def send_add_onclick(e):
    
    
    csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value
    number = document.getElementById('lome').value;
    body = json.dumps({'number': number})
    headers = {'X-CSRFToken' : csrf}
    data = await make_request(url='/hel',method='POST', body=body,headers=headers)
    ul = document.getElementById('me')
    ul.innerHTML = data['data']


def mes():
    button1 = document.getElementById('bu{{forloop.counter}}')
    button1.addEventListener('click',pyodide.create_proxy(send_add_onclick))

mes()