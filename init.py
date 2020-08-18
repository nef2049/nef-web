import os


if __name__ == "__main__":
    os.system('rm -rf jekyll-theme-chirpy/')
    os.system('rm -rf static/user/')

    os.system('sudo cp nefvision-nginx.conf /etc/nginx/conf.d/')
    os.system('sudo /etc/init.d/nginx restart')
