def ws(environ, start_response):
    
   status = '200 OK'
   headers = [
       ('Content-Type', 'text/plain')
   ]
   body = ''
   for key in environ:
       body = body + str(environ[key]) + '\n'
   body.replace('&', '\n')

   start_response(status, headers)
   return body
