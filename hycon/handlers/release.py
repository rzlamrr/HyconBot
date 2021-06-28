# This file is part of Hycon (Telegram Bot)

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import json
import os

import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from hycon.config import UPDATES_CHANEL

from .devices import check_device

DEVICES_REPO = "https://raw.githubusercontent.com/Hycon-Devices/official_devices/master"


@Client.on_message(filters.sudo & filters.cmd("release (?P<ver>.+) (?P<codename>.+)"))
async def release_m(c: Client, m: Message):
    vtag = m.matches[0]["ver"]
    codename = m.matches[0]["codename"]
    model = check_device(codename)
    try:
        file_path = await c.download_media(message=m.reply_to_message)
    except Exception:
        return await m.reply_text(text=f"Reply to media!")
    if not model:
        return await m.reply_text(text=f"The device <b>{codename}</b> was not found!")
    t = await m.reply_text("Processing")
    models = json.loads(requests.get(DEVICES_REPO + "/devices.json").text)
    for m in models:
        if m["codename"] == codename:
            depis = m["name"]
            for n in m["supported_versions"]:
                maintainer = n["maintainer_name"]
                vname = n["version_name"]
                vcode = n["version_code"]
                xda = n["xda_thread"]
    await t.edit(text=f"Device: {depis}")
    vcode = v_code(vcode)

    data = json.loads(requests.get(DEVICES_REPO + f"/builds/{codename}.json").text)
    for item in data:
        filename = item["filename"]

    changelogs = (
        f"https://github.com/HyconOS-Releases/{codename}/blob/main/devicechangelog.md"
    )
    source = "https://github.com/HyconOS-Releases/Source_Changelog#readme"
    durl = f"https://www.pling.com/p/1544683/"

    text = f"#Hycon #Official #{vcode} #{codename}\n\n"
    text += f"Hycon OS {vtag} | {vname} | {depis}\n"
    text += f"Changelog: [Device]({changelogs}) | [Source]({source})\n\n"
    text += f"Maintainer: {maintainer}"
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("XDA", url=f"{xda}"),
                InlineKeyboardButton("Download", url=f"{durl}"),
            ]
        ]
    )

    try:
        await c.send_photo(
            chat_id=UPDATES_CHANEL,
            photo=file_path,
            caption=text,
            reply_markup=keyboard,
            parse_mode="md",
        )
    except Exception as e:
        await t.edit(text="!!FAILED: " + str(e))
    os.remove(file_path)


def v_code(arg):
    ver = {"nine": "A9", "ten": "A10", "eleven": "A11", "twelve": "A12"}
    return ver.get(arg, "A11")
