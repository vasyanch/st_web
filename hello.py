def ws(environ, start_response):
    
   status = '200 OK'
   headers = [
       ('Content-Type', 'text/plain')
   ]
   body = [i for i in environ['QUERY_STRING'].split('&')]

   start_response(status, headers)
   return body




