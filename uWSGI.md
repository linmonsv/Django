    75  yum -y install epel-release
    76  yum -y install python-pip
    77  yum clean all
    
    88  yum install  -y vim  wget gcc gcc-c++ zlib-devel libxml2-devel libxslt-devel libffi python-cffi libffi-devel  openssl openssl-devel bzip2-devel ncurses-devel sqlite-devel sqlite 
    93  yum install python-devel.x86_64
    95  pip install uwsgi
    
    105  cat test.py 
```python
def application(env, start_response):
        start_response('200 OK', [('Context-Type', 'text/html')])
        return "Hello World!"
```

    106  vim test.py 
    107  uwsgi --http :8001 --wsgi-file test.py
