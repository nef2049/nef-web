> About

```txt
    https://jekyllrb.com/docs/installation/ubuntu/
    https://github.com/cotes2020/jekyll-theme-chirpy/
```

> Usage

```bash
pip3 install flask
pip3 install pymysql
pip3 install pyyml

sudo python3 init.py
python3 run.py
```

> example

```
http://119.45.209.174:2333
```

> url

```
// upload favicon
curl -X POST -F "file=@/c/Users/Vaadhoo/Desktop/0cc396138b4990e8bd5cf76cd4177d24.ico.zip" http://10.0.75.1:2333/bc/461947432927788/upload

// upload post
 curl -X POST -F "file=@/c/Users/Vaadhoo/Desktop/2020-08-24-boost-asio-io-service.md" http://10.0.75.1:2333/user/upload/461947432927788

// To be continued...
...
```