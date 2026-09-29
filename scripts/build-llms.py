#!/usr/bin/env python3
"""Genera llms.txt e llms-full.txt dalle pagine HTML del sito.

Uso (dalla root del repo):  python3 scripts/build-llms.py

- llms.txt      : indice in Markdown del sito per gli assistenti AI (chi è Emma,
                  i percorsi, gli articoli, i contatti). Standard: https://llmstxt.org/
- llms-full.txt : lo stesso indice + il testo integrale delle pagine indicizzabili.

Rilanciare dopo ogni modifica sostanziale ai testi o quando si aggiunge un articolo.
Solo libreria standard, nessuna dipendenza.
"""
import html
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://emma-allenamente.com"

# (path, sezione) — solo pagine indicizzabili, nell'ordine in cui vanno presentate
PAGES = [
    ("index.html", "Home"),
    ("chi-sono.html", "Chi sono"),
    ("psicologo-online-adolescenti.html", "Percorsi"),
    ("ansia-scolastica.html", "Percorsi"),
    ("ansia-giovani-adulti.html", "Percorsi"),
    ("autostima-adolescenti.html", "Percorsi"),
    ("blog/index.html", "Blog"),
]


def read(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as f:
        return f.read()


def meta(src, name):
    m = re.search(r'<meta name="%s" content="([^"]*)"' % name, src) or re.search(r'<meta property="%s" content="([^"]*)"' % name, src)
    return html.unescape(m.group(1)) if m else ""


def title(src):
    m = re.search(r"<title>(.*?)</title>", src, re.S)
    return html.unescape(m.group(1).strip()) if m else ""


def main_text(src):
    """Testo del <main>, con i titoli resi come intestazioni Markdown."""
    m = re.search(r"<main>(.*?)</main>", src, re.S)
    body = m.group(1) if m else src
    body = re.sub(r"<!--.*?-->", "", body, flags=re.S)
    body = re.sub(r"<form.*?</form>", "", body, flags=re.S)
    body = re.sub(r"<nav class=\"breadcrumb\".*?</nav>", "", body, flags=re.S)
    body = re.sub(r"<(script|style|svg)[^>]*>.*?</\1>", "", body, flags=re.S)
    for lvl in (1, 2, 3, 4):
        body = re.sub(r"<h%d[^>]*>(.*?)</h%d>" % (lvl, lvl), lambda m, l=lvl: "\n\n" + "#" * l + " " + re.sub(r"<[^>]+>", "", m.group(1)).strip() + "\n\n", body, flags=re.S)
    body = re.sub(r"<summary[^>]*>(.*?)</summary>", lambda m: "\n\n**" + re.sub(r"<[^>]+>", "", m.group(1)).strip() + "**\n\n", body, flags=re.S)
    body = re.sub(r"<li[^>]*>", "\n- ", body)
    body = re.sub(r"</(p|li|div|section|article|aside|details|dd|dt|ol|ul)>", "\n", body)
    body = re.sub(r"<br\s*/?>", "\n", body)
    body = re.sub(r"<[^>]+>", "", body)
    body = html.unescape(body)
    body = re.sub(r"[ \t]+", " ", body)
    body = "\n".join(l.strip() for l in body.splitlines())
    body = re.sub(r"\n\s*\n\s*\n+", "\n\n", body)
    return body.strip()


def blog_posts():
    posts = []
    bdir = os.path.join(ROOT, "blog")
    for f in sorted(os.listdir(bdir)):
        if f.endswith(".html") and f != "index.html":
            src = read("blog/" + f)
            posts.append(("blog/" + f, title(src).split("|")[0].strip(), meta(src, "description")))
    return posts


def build():
    pages = []
    for path, section in PAGES:
        src = read(path)
        pages.append((path, section, title(src), meta(src, "description"), main_text(src)))
    posts = blog_posts()

    index = []
    index.append("# Emma Veronesi — Psicologa online per adolescenti e giovani adulti\n")
    index.append("> La Dott.ssa Emma Veronesi è una psicologa iscritta all'Ordine degli Psicologi della Lombardia (n. 32092), laureata all'Università Cattolica del Sacro Cuore di Milano. Lavora esclusivamente online, in videochiamata, con adolescenti (dai 13 anni) e giovani adulti (fino ai 30 circa) in tutta Italia, su ansia, ansia scolastica e da esame, autostima, gestione delle emozioni e relazioni. Il primo colloquio conoscitivo, di circa 30 minuti, è gratuito. Per i minorenni serve il consenso dei genitori. Il suo progetto di divulgazione su Instagram e TikTok si chiama Allenamente (@allenamente.emma).\n")
    index.append("Sito: " + SITE + "/ · Lingua: italiano · Contatto: form sul sito (" + SITE + "/#contatta)\n")
    for section in ("Chi sono", "Percorsi", "Blog"):
        index.append(f"\n## {section}\n")
        for path, sec, t, d, _ in pages:
            if sec == section:
                index.append(f"- [{t.split('|')[0].strip()}]({SITE}/{path}): {d}")
        if section == "Blog":
            for path, t, d in posts:
                index.append(f"- [{t}]({SITE}/{path}): {d}")
    index.append("\n## Informazioni legali\n")
    index.append(f"- [Privacy Policy]({SITE}/privacy.html)")
    index.append(f"- [Cookie Policy]({SITE}/cookie.html)")
    index.append("\n## Profili ufficiali\n")
    index.append("- Instagram: https://www.instagram.com/allenamente.emma/")
    index.append("- TikTok: https://www.tiktok.com/@allenamente.emma")
    index.append("- LinkedIn: https://www.linkedin.com/in/emma-veronesi/")
    index.append("- Verifica iscrizione all'Albo (OPL): https://www.opl.it/iscritti-ricerca-avanzata.php")
    llms = "\n".join(index) + "\n"

    full = [llms, "\n---\n"]
    for path, sec, t, d, text in pages:
        full.append(f"\n\n# {t}\n\nURL: {SITE}/{path}\n\n{text}\n")
    for path, t, d in posts:
        src = read(path)
        full.append(f"\n\n# {t}\n\nURL: {SITE}/{path}\n\n{main_text(src)}\n")
    llms_full = "".join(full)

    with open(os.path.join(ROOT, "llms.txt"), "w", encoding="utf-8") as f:
        f.write(llms)
    with open(os.path.join(ROOT, "llms-full.txt"), "w", encoding="utf-8") as f:
        f.write(llms_full)
    print(f"llms.txt: {len(llms.split())} parole · llms-full.txt: {len(llms_full.split())} parole")


if __name__ == "__main__":
    build()
