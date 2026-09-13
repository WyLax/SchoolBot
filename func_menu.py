from aiogram.types import FSInputFile


async def menu():
    filename = ("photo_menu/menu.jpg")
    return FSInputFile(filename)

