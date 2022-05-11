# File_Server_Client

## Sample code to mock the file server firmware update procedure
 
> Navigate to 'server' directory:
- execute **start_local_file_server.bat** file

> Navigate to client directory:
```
pip install -r requirements.txt
python test.py -u "http://127.0.0.1:80/" -f "1.0.2"
```

- -u: File Server Url
- -f: Current firmware version installed

You can edit [test file](client/test.py) for changing the file download option to False
