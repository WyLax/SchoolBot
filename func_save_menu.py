import io
import aiohttp
import pymupdf
from PIL import Image


MENU_URL_1_11 = "https://22-vp.ru/food22/egednevnoe_menu1-11.pdf"
MENU_URL_5_11 = "https://22-vp.ru/food22/egednevnoe_menu5-11.PDF"


async def save_menu():

    proxy_url = "http://45.132.252.25:49156"

    async with aiohttp.ClientSession() as session:
        async with session.get(MENU_URL_1_11, proxy=proxy_url) as response:
            if response.status == 200:
                pdf_data = await response.read()
            else:
                async with session.get(MENU_URL_5_11, proxy=proxy_url) as response:
                pdf_data = await response.read()


    pdf = pymupdf.open(stream=pdf_data, filetype="pdf")

    images = []

    for page in pdf:
        image_list = page.get_images(full=True)

        if not image_list:
            continue

        xref = image_list[0][0]
        image_data = pdf.extract_image(xref)["image"]

        image = Image.open(io.BytesIO(image_data)).convert("RGB")
        images.append(image)

    pdf.close()

    width = sum(image.width for image in images)
    height = max(image.height for image in images)

    result = Image.new("RGB", (width, height), "white")

    x = 0
    for image in images:
        result.paste(image, (x, 0))
        x += image.width



    result.thumbnail((1600,1600))
    result.save("photo_menu/menu.jpg", format="JPEG", quality=80)
