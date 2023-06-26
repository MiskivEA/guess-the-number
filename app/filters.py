from typing import List

from aiogram import types
from aiogram.filters import BaseFilter


# class IsAdmin(BaseFilter):
#     def __init__(self, admin_ids: List) -> None:
#         self.admin_ids = admin_ids
#
#     async def __call__(self, message: types.Message) -> bool:
#         return message.from_user.id in self.admin_ids
