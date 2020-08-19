import os


if __name__ == "__main__":
    os.system('rm -rf jekyll-theme-chirpy/')
    os.system('rm -rf static/user/')

    """
    sudo nginx -s stop &&  
    sudo cp nefvision-nginx.conf /usr/local/nginx/conf/ && 
    sudo nginx -c /usr/local/nginx/conf/nefvision-nginx.conf && 
    sudo nginx -s reopen
    """
    os.system('sudo nginx -s stop')
    os.system('sudo cp {} {}'.format("nefvision-nginx.conf", "/usr/local/nginx/conf/"))
    os.system('sudo nginx -c /usr/local/nginx/conf/{}'.format("nefvision-nginx.conf"))
    os.system('sudo nginx -s reopen')
