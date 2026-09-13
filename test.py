import asyncio
from func_save_screen import save_screen


async def main():
    await save_screen("понедельник",
                      "https://docs.google.com/spreadsheets/d/1VofWY1vYGFHP-KGirs-0C84YOACDfp_rWkhJJP3Hpls/edit?gid=90085117#gid=90085117")

if __name__ == "__main__":
    asyncio.run(main())