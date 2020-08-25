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

> Example

```
http://119.45.209.174:2333
```

> url

```
// upload favicon
curl -X POST -F "file=@/c/Users/Vaadhoo/Desktop/0cc396138b4990e8bd5cf76cd4177d24.ico.zip" http://119.45.209.174:2333/bc/<user_id>/upload

// upload post
curl -X POST -F "file=@/c/Users/Vaadhoo/Desktop/2020-08-24-boost-asio-io-service.md" http://119.45.209.174:2333/user/upload/<user_id>

// update info
curl -X POST -d "title=Sleep Zeo&&tagline=Now is everything&&author=nef&&github_username=sleepy-zeo&&twitter_username=sleepy_zeo&&social_name=nef&&social_email=steven199409@outlook.com&&social_links=https://twitter.com/NEF2049;https://weibo.com/5310322716/profile?rightmod=1&wvr=6&mod=personinfo&is_all=1&&url=http://119.45.209.174:2333" -H "Content-Type: application/x-www-form-urlencoded" http://119.45.209.174:2333/bc/<user_id>/update

// upload avatar
curl -X POST -F "file=@/c/Users/Vaadhoo/Desktop/1023.jpg" http://119.45.209.174:2333/images/upload/<user_id>/avatar

// To be continued...
...
```
