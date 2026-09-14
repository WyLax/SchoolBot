import asyncio
import io

from aiogram import Bot, types
from aiogram.types import FSInputFile
from os import remove
from PIL import Image
from playwright.async_api import async_playwright


async def save_screen(way, url, timeout=40):
    filename = (f"photo_schedule/{way}.png")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.set_viewport_size({"width": 1680, "height": 1850})
        await page.goto(url, timeout=timeout * 1000)
        await page.evaluate("document.body.style.zoom='1'")
        png_data = await page.screenshot(full_page=True)

        img = Image.open(io.BytesIO(png_data))
        width, height = img.size
        left = 46
        upper = 167

        lower = height  # Изначально устанавливаем lower как нижнюю границу

        # Поиск первого черного пикселя снизу
        for y in range(height - 1, 0, -1):
            for x in range(left, width):  # Итерируемся до правого края
                r, g, b, *_ = img.getpixel((x, y))
                if r == 0 and g == 0 and b == 0:
                    lower = y + 1
                    break  # Выходим из внутреннего цикла, если нашли черный пиксель
            if lower != height:  # Выходим из внешнего цикла, если lower изменилось
                break

        # Поиск первого черного пикселя справа
        right = width  # Изначально устанавливаем right как правый край

        black_pixel_found = False
        for x in range(width - 1, 0, -1):
            for y in range(upper, lower):
                r, g, b, *_ = img.getpixel((x, y))
                if r == 0 and g == 0 and b == 0:
                    right = x + 1
                    black_pixel_found = True
                    break
            if black_pixel_found:
                break

        img_cropped = img.crop((left, upper, right-1, lower-1))
        img_cropped.save(filename)
        await browser.close()

        return FSInputFile(filename)
