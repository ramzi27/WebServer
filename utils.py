CONTENT_TYPES={
    ".json":"application/json",
    ".js":"application/javascript",
    ".pdf":"application/pdf",
    ".xml":"application/xml",

    #images
    ".gif":"image/gif",
    ".jpeg":"image/jpeg",
    ".png":"image/png",

    #text:
    ".css":"text/css",
    ".csv":"text/csv",
    ".html":"text/html",
    ".txt":"text/plain; charset=UTF-8",

    #video
    ".mpeg":"video/mpeg",
    ".mp4":"video/mp4"
}

SUCCESS_HEADER="""
HTTP/1.1 200 OK
Content-Type:%s
Server: Ramzi-Server/1.0
content-length:%s

"""
#new line for body
NOT_FOUND_HEADER="""
HTTP/1.1 404 NOT FOUND
Content-Type:text/html
Server: Ramzi-Server/1.0

<html> 
<head><title>Not Found</title></head>
<body>Not Found</body></html>
"""

POST_UNSUPPORTED_HEADER="""
HTTP/1.1 404 NOT FOUND
Content-Type:text/html
Server: Ramzi-Server/1.0

<html> 
<head><title>POST Unsupoorted/title></head>
<body>POST Request Is Unsupported</body></html>
"""



