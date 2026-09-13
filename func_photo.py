from aiogram.types import FSInputFile


async def photo(day):
    filename = (f"photo_schedule/{day}.png")
    return FSInputFile(filename)

