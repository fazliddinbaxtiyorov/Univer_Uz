/**
 * UniBase — Language Switcher
 * Django i18n bilan ishlaydi: til o'zgarganda server session yangilanadi,
 * sahifa reload bo'ladi va BUTUN LOYIHA yangi tilda ko'rinadi.
 */

const STORAGE_KEY = "unibase_lang";
const SET_LANG_URL = "/i18n/set-language/";

/**
 * Tilni o'zgartiradi:
 *  1. Django serveriga POST — session + cookie yangilanadi
 *  2. Sahifa reload — barcha {% trans %} yangi tilda chiqadi
 */
async function switchLanguage(lang) {
  try {
    // CSRF token olish (Django talab qiladi)
    const csrf = getCookie("csrftoken");

    await fetch(SET_LANG_URL, {
      method: "POST",
      headers: {
        "Content-Type":  "application/json",
        "X-CSRFToken":   csrf || "",
      },
      body: JSON.stringify({ lang }),
    });
  } catch (err) {
    console.warn("[UniBase] set_language request failed:", err);
  }

  // Session da saqlangan, sahifani reload qilamiz
  localStorage.setItem(STORAGE_KEY, lang);
  window.location.reload();
}

/** Django CSRF cookie ni o'qiydi */
function getCookie(name) {
  const val = `; ${document.cookie}`;
  const parts = val.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
  return null;
}

/** Sahifa ochilganda selector ni to'g'ri qiymatga o'rnatadi */
function syncSelector() {
  const selector = document.getElementById("language-selector");
  if (!selector) return;

  // Django <html lang="..."> dan yoki cookie dan olamiz
  const htmlLang = document.documentElement.lang?.slice(0, 2) || "en";
  const saved    = localStorage.getItem(STORAGE_KEY) || htmlLang;

  if (["en", "ru", "uz"].includes(saved)) {
    selector.value = saved;
  }

  selector.addEventListener("change", (e) => {
    switchLanguage(e.target.value);
  });
}

document.addEventListener("DOMContentLoaded", syncSelector);

// Global export
window.UniBaseLang = { switchLanguage };