# Ultron Python client


## Install

Install via pip

    pip install https://github.com/KitchenStories/python-ultron-client.git
    
## Usage


```python
# Import
from ultron_client.clients import FlaskUltronAsyncService
from flask import request

# Create new Service with desired paralell workers 
ultron = FlaskUltronAsyncService(request, max_workers=2, stage=STAGE)

# Enqueue get-requests with additional parameters
# The key is needed to remap async results
ultron.get('comments', '/api/users/comments/', parameters=request.args)
ultron.get('gallery', '/api/users/comments/images/', parameters=request.args)

# Fetch and wait until all requests finishes
results = ultron.results()

# Forwarding ultron headers
response = ultron.make_flask_response('NEW CONTENT')

```

