import urllib.request

api_token = "fklasjfljasdlkfjlasjflasjfljhasdljflsdjflkjsadljfljsda"


def download_img(img_url, api_token=api_token):
    header = {"Authorization": "Bearer " + api_token}  # 设置http header
    request = urllib.request.Request(img_url, headers=header)
    try:
        response = urllib.request.urlopen(request)
        img_name = "img.png"
        if response.getcode() == 200:
            with open(img_name, "wb+") as f:
                f.write(response.read())  # 将内容写入图片
            return img_name
    except:
        return "failed"
