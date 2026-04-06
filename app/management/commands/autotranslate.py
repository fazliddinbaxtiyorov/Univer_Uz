# management/commands/autotranslate.py
#
# gettext o'rnatilmasa ham ishlaydi!
# Gemini API bilan .po tarjima qiladi (BATCH - 1 so'rovda hammasi),
# .mo faylni Python ichida compile qiladi.

import os
import re
import sys
import time
import json
import struct
import subprocess
from pathlib import Path

from google import genai

from django.core.management.base import BaseCommand
from django.conf import settings


GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", getattr(settings, "GEMINI_API_KEY", ""))

LANG_NAMES = {"ru": "Russian", "uz": "Uzbek"}


# ── Gemini BATCH tarjima (1 so'rovda hammasi) ────────────────────────────────

def gemini_translate_batch(texts: list[str], target_lang: str, retries: int = 5) -> dict | None:
    """
    Barcha matnlarni bitta API chaqiruvida tarjima qiladi.
    Qaytaradi: {original_text: translated_text, ...}
    """
    client    = genai.Client(api_key=GEMINI_API_KEY)
    lang_name = LANG_NAMES.get(target_lang, target_lang)

    # JSON formatda yuborish
    numbered = {str(i): t for i, t in enumerate(texts)}
    prompt = (
        f"Translate the following JSON values to {lang_name}.\n"
        f"Rules:\n"
        f"- Return ONLY valid JSON, nothing else\n"
        f"- Keep the same keys (numbers)\n"
        f"- Keep emojis as-is\n"
        f"- Keep technical terms (IELTS, SAT, DTM, UniBase) as-is\n"
        f"- Keep © symbol as-is\n"
        f"- No explanations, no markdown, no backticks\n\n"
        f"{json.dumps(numbered, ensure_ascii=False)}"
    )

    for attempt in range(1, retries + 1):
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt,
            )
            raw = response.text.strip()

            # JSON ni tozalash (backtick bo'lsa)
            raw = re.sub(r"^```[a-z]*\n?", "", raw)
            raw = re.sub(r"\n?```$", "", raw)
            raw = raw.strip()

            translated_dict = json.loads(raw)

            # {original: translation} formatga o'tkazish
            result = {}
            for i, original in enumerate(texts):
                key = str(i)
                if key in translated_dict:
                    result[original] = translated_dict[key]
            return result

        except json.JSONDecodeError as e:
            print(f"    ⚠️  JSON parse xato (urinish {attempt}/{retries}): {e}")
            time.sleep(3)
            continue

        except Exception as e:
            err_str = str(e)
            if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str:
                wait = 65
                match = re.search(r"retryDelay.*?(\d+)s", err_str)
                if match:
                    wait = int(match.group(1)) + 10
                print(f"    ⏳ Rate limit! {wait}s kutilmoqda... (urinish {attempt}/{retries})")
                time.sleep(wait)
                continue

            print(f"    ⚠️  Gemini xato: {e}")
            return None

    print(f"    ❌ {retries} urinishdan keyin ham ishlamadi")
    return None


# ── .po parser ───────────────────────────────────────────────────────────────

def parse_po(filepath: Path):
    text    = filepath.read_text(encoding="utf-8")
    entries = []
    pattern = re.compile(
        r'(msgid\s+"((?:[^"\\]|\\.)*)"\nmsgstr\s+"((?:[^"\\]|\\.)*)")',
        re.MULTILINE,
    )
    for m in pattern.finditer(text):
        msgid  = m.group(2)
        msgstr = m.group(3)
        if msgid:
            entries.append({
                "full":   m.group(1),
                "msgid":  msgid,
                "msgstr": msgstr,
            })
    return entries, text


def fill_po(filepath: Path, lang: str, force: bool = False):
    entries, text = parse_po(filepath)

    # Tarjima qilinmagan entrylarni topish
    to_translate = [e for e in entries if not e["msgstr"] or force]
    skipped      = len(entries) - len(to_translate)

    if not to_translate:
        print(f"    ℹ️  Hamma matn tarjima qilingan, --force ishlating")
        return 0, skipped

    msgids = [e["msgid"] for e in to_translate]
    print(f"    📦 {len(msgids)} ta matn bitta so'rovda yuborilmoqda...")

    translations = gemini_translate_batch(msgids, lang)
    if not translations:
        print(f"    ❌ Tarjima olinmadi")
        return 0, skipped

    changed = 0
    for entry in to_translate:
        translated = translations.get(entry["msgid"])
        if not translated:
            print(f"    ⚠️  SKIP: {entry['msgid'][:50]}")
            continue
        escaped   = translated.replace('\\', '\\\\').replace('"', '\\"')
        new_block = f'msgid "{entry["msgid"]}"\nmsgstr "{escaped}"'
        text      = text.replace(entry["full"], new_block, 1)
        changed  += 1
        print(f"    ✅ {entry['msgid'][:38]:38s} → {translated[:38]}")

    filepath.write_text(text, encoding="utf-8")
    return changed, skipped


# ── Pure Python .mo compiler ─────────────────────────────────────────────────

def compile_po_to_mo(po_path: Path) -> Path:
    entries, _ = parse_po(po_path)
    pairs = [(e["msgid"], e["msgstr"]) for e in entries if e["msgstr"]]

    MAGIC      = 0x950412de
    VERSION    = 0
    n          = len(pairs)
    offset_ids = 28
    offset_str = offset_ids + 8 * n

    ids  = b""
    strs = b""
    id_offsets  = []
    str_offsets = []

    for msgid, msgstr in pairs:
        id_bytes  = msgid.encode("utf-8")
        str_bytes = msgstr.encode("utf-8")
        id_offsets.append((len(id_bytes),  offset_ids  + 8 * n + len(ids)))
        str_offsets.append((len(str_bytes), offset_str + len(strs)))
        ids  += id_bytes  + b"\x00"
        strs += str_bytes + b"\x00"

    buf = struct.pack("<IIIIIII", MAGIC, VERSION, n, offset_ids, offset_str, 0, 0)
    for length, offset in id_offsets:
        buf += struct.pack("<II", length, offset)
    for length, offset in str_offsets:
        buf += struct.pack("<II", length, offset)
    buf += ids + strs

    mo_path = po_path.with_suffix(".mo")
    mo_path.write_bytes(buf)
    return mo_path


# ── gettext PATH fix ──────────────────────────────────────────────────────────

def ensure_gettext_in_path():
    result = subprocess.run(["msguniq", "--version"], capture_output=True, shell=True)
    if result.returncode == 0:
        return True
    for p in [
        r"C:\Program Files\gettext-iconv\bin",
        r"C:\Program Files (x86)\gettext-iconv\bin",
        r"C:\gettext\bin",
    ]:
        if Path(p, "msguniq.exe").exists():
            os.environ["PATH"] = p + os.pathsep + os.environ.get("PATH", "")
            return True
    return False


# ── Management command ───────────────────────────────────────────────────────

class Command(BaseCommand):
    help = "Gemini AI bilan .po tarjima (BATCH) + Python da .mo compile"

    def add_arguments(self, parser):
        parser.add_argument("--lang",       default="all")
        parser.add_argument("--force",      action="store_true")
        parser.add_argument("--no-make",    action="store_true")
        parser.add_argument("--no-compile", action="store_true")

    def handle(self, *args, **options):
        lang_arg   = options["lang"]
        force      = options["force"]
        langs      = ["ru", "uz"] if lang_arg == "all" else [lang_arg]
        locale_dir = Path(settings.BASE_DIR) / "locale"
        locale_dir.mkdir(exist_ok=True)

        if not GEMINI_API_KEY:
            self.stdout.write(self.style.ERROR(
                "\n❌ GEMINI_API_KEY topilmadi!\n"
                "settings.py ga qo'shing: GEMINI_API_KEY = 'AIza...'\n"
                "Yangi key: https://aistudio.google.com\n"
            ))
            return
        self.stdout.write(self.style.SUCCESS("✔  Gemini API key topildi\n"))

        # ── 1. makemessages ──────────────────────────────────────────────
        if not options["no_make"]:
            self.stdout.write("🔍  Templatelardan matnlar yig'ilmoqda...")
            ensure_gettext_in_path()
            for lang in langs:
                result = subprocess.run(
                    [sys.executable, "manage.py", "makemessages",
                     "-l", lang, "--no-wrap"],
                    capture_output=True, text=True,
                    cwd=str(settings.BASE_DIR),
                    env=os.environ.copy(),
                )
                if result.returncode != 0:
                    self.stdout.write(self.style.WARNING(
                        f"⚠️  makemessages [{lang}] ishlamadi — .po fayllar mavjud bo'lsa davom etadi.\n"
                    ))
            self.stdout.write(self.style.SUCCESS("✔  makemessages bosqichi tugadi\n"))

        # ── 2. Gemini BATCH bilan .po to'ldirish ─────────────────────────
        for lang in langs:
            po_path = locale_dir / lang / "LC_MESSAGES" / "django.po"
            if not po_path.exists():
                self.stdout.write(self.style.WARNING(f"\n⚠️  {po_path} topilmadi.\n"))
                continue

            entries, _ = parse_po(po_path)
            empty = sum(1 for e in entries if not e["msgstr"])
            self.stdout.write(
                f"\n🤖  [{lang.upper()}] Gemini BATCH tarjima "
                f"({empty} bo'sh / {len(entries)} jami)..."
            )
            changed, skipped = fill_po(po_path, lang, force=force)
            self.stdout.write(self.style.SUCCESS(
                f"✔  [{lang.upper()}] {changed} yangi, {skipped} mavjud\n"
            ))

        # ── 3. .mo compile ───────────────────────────────────────────────
        if not options["no_compile"]:
            self.stdout.write("⚙️   .mo fayllar compile qilinmoqda...")
            for lang in langs:
                po_path = locale_dir / lang / "LC_MESSAGES" / "django.po"
                if not po_path.exists():
                    continue
                try:
                    mo_path = compile_po_to_mo(po_path)
                    self.stdout.write(self.style.SUCCESS(f"    ✅ {mo_path}"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"    ❌ [{lang}] .mo xato: {e}"))

            self.stdout.write(self.style.SUCCESS(
                "\n✔  Hammasi tayyor! Server restart qiling:\n"
                "   Ctrl+C → python manage.py runserver\n"
            ))