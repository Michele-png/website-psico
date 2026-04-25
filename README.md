# Sito web — Emma Veronesi, Psicologa

Sito statico professionale ospitato su GitHub Pages.

- Stack: HTML + CSS + JavaScript vanilla. Zero build, zero dipendenze.
- Hosting: GitHub Pages (gratuito).
- Form di contatto: Web3Forms (gratuito, server EU).

---

## Parte 1 — Guida per Emma

### Come modificare i testi del sito

Il sito è composto da pochi file con i testi al loro interno. Puoi modificarli direttamente da GitHub.com, senza installare nulla.

#### Quale file contiene cosa

| Cosa vuoi cambiare | File da aprire |
|---|---|
| Testo della home (hero, sezione "Conosci Emma", servizi, form) | `index.html` |
| Privacy Policy | `privacy.html` |
| Cookie Policy | `cookie.html` |
| Pagina di errore 404 | `404.html` |

#### Procedura (3 minuti)

1. Vai su [github.com/Michele-png/website-psico](https://github.com/Michele-png/website-psico).
2. Clicca sul file che vuoi modificare (es. `index.html`).
3. In alto a destra del file, clicca sull'icona della **matita** ("Edit this file").
4. **Cerca** la parte da cambiare con `Ctrl+F` (Windows) o `Cmd+F` (Mac). Tutto il sito ha sezioni segnalate da commenti del tipo:
   ```
   <!-- =========================================================
        SEZIONE EMMA — chi è Emma, formazione, approccio
        ========================================================= -->
   ```
   Cerca per esempio "SEZIONE EMMA" e arrivi subito al punto giusto.
5. Modifica solo il testo. **Non toccare** le parentesi angolari `<` `>` né i `class="..."`.
6. Quando hai finito, scorri in fondo, scrivi un breve messaggio nel campo "Commit changes" (es. "Aggiornato bio") e clicca il bottone verde **"Commit changes"**.
7. In ~30 secondi il sito è aggiornato.

#### Modificare con l'aiuto di un LLM (consigliato)

Se non vuoi fare a mano, puoi usare ChatGPT/Claude/Gemini:

1. Apri il file su GitHub e clicca **"Copy raw file"**.
2. Incolla il contenuto in chat all'LLM scrivendo qualcosa come:
   > Ti incollo qui sotto il file `index.html` del mio sito. Modifica la frase "Sono laureata in..." sostituendola con "Sono laureata in [nuovo testo]". Restituiscimi il file completo modificato.
3. Copia la risposta dell'LLM e incollala nuovamente nell'editor di GitHub al posto del contenuto precedente.
4. Commit.

#### Cose che si possono modificare in autonomia

✅ Tutti i testi (titoli, paragrafi, etichette dei bottoni, etichette del form)
✅ Aggiungere o togliere un valore tra i 4 box "Cosa puoi aspettarti"
✅ Aggiungere o togliere una card tra i servizi (copia/cancella un blocco `<article class="servizio-card">...</article>`)
✅ Cambiare il numero dei passi in "Come funziona"
✅ Modificare il footer (P.IVA, link social, pagine legali)

#### Cose da NON modificare in autonomia

❌ I file dentro `assets/css/` o `assets/js/` (è il "motore" del sito)
❌ Le strutture HTML come `class="..."`, `id="..."`, `<div>`, `<section>`
❌ Il file `assets/js/config.js` (contiene chiavi tecniche)

Se hai dubbi, scrivi a Michele.

#### Cambiare le foto

1. Sostituisci i file dentro `assets/img/` mantenendo lo stesso nome:
   - `emma-portrait.jpg` (ritratto in sezione "Conosci Emma")
   - `camelia.jpg` (foto della camelia nell'hero, larga)
   - `camelia-small.jpg` (versione piccola usata come decorazione)
2. **Importante**: le foto devono essere in formato JPG e idealmente sotto 300 KB ciascuna per non rallentare il sito.
3. Per il ritratto: rapporto 4:5 verticale (es. 800x1000 px).
4. Per la camelia: rapporto 3:4 verticale (es. 1200x1600 px).

---

## Parte 2 — Setup tecnico (Michele)

### Cose da fare al primo deploy

#### 1. Attivare GitHub Pages

Il repo è pubblico e GitHub Pages è già configurato da `main / (root)`.
Il sito live è `https://michele-png.github.io/website-psico/`.

#### 2. Configurare Web3Forms (form di contatto)

1. Vai su [web3forms.com](https://web3forms.com/), clicca **"Create your Access Key"**.
2. Inserisci l'email di Emma (è dove arriveranno i messaggi; per ora la Gmail personale non è mostrata pubblicamente sul sito).
3. Riceverai una chiave via email (un UUID tipo `a1b2c3d4-...`).
4. Apri `assets/js/config.js`, sostituisci `INSERISCI-QUI-LA-CHIAVE-WEB3FORMS` con la chiave reale.
5. Commit + push.
6. Test: invia un messaggio dal form e verifica che arrivi all'email di Emma.

#### 3. Configurare WhatsApp

In `assets/js/config.js`, il campo `whatsapp.numero` è volutamente vuoto: il bottone resta visibile ma disabilitato.
Quando avrai il vero numero WhatsApp di Emma, inseriscilo in formato internazionale senza `+` (es. `393331234567`).

#### 4. Completare la P.IVA

Cerca `P.IVA da inserire` nei file `index.html`, `privacy.html` e `cookie.html`, poi sostituiscilo con la Partita IVA reale di Emma.
Il numero Albo è già aggiornato: `32092`.

### Aggiungere un dominio custom (in seguito)

Quando comprerai il dominio (consigliati: [Aruba](https://www.aruba.it) o [Register.it](https://www.register.it/), ~10€/anno per `.it`):

1. Crea un file `CNAME` nella root del repo con dentro solo `emmaveronesi.it` (senza `https://` né `www`).
2. Sul tuo provider DNS (Aruba/Register), configura:
   - 4 record **A** che puntano a:
     ```
     185.199.108.153
     185.199.109.153
     185.199.110.153
     185.199.111.153
     ```
   - 1 record **CNAME** per `www` che punta a `michele-png.github.io`.
3. Su GitHub: Settings → Pages → Custom domain → inserisci `emmaveronesi.it` → Save → spunta "Enforce HTTPS" (dopo che la verifica DNS è completata, ~10 min - 24 h).
4. Aggiorna il dominio GitHub Pages nella Privacy Policy con il dominio custom scelto.

### Email professionale gratuita (in seguito)

Quando avrai il dominio, attiva [Cloudflare Email Routing](https://www.cloudflare.com/products/email-routing/):

1. Sposta il DNS del dominio su Cloudflare (gratis).
2. Email Routing → Add address → `info@emmaveronesi.it` inoltra a → Gmail di Emma.
3. Costo: 0€.

### Struttura del progetto

```
website-psico/
├── index.html              # Home: hero + Emma + Servizi + Contatta
├── privacy.html            # Privacy Policy
├── cookie.html             # Cookie Policy
├── 404.html                # Pagina di errore brandizzata
├── README.md               # Questo file
├── assets/
│   ├── css/styles.css      # Tutti gli stili + design tokens
│   ├── js/
│   │   ├── config.js       # Chiavi tecniche (Web3Forms, WhatsApp)
│   │   └── main.js         # Logica del sito
│   └── img/
│       ├── emma-portrait.jpg
│       ├── camelia.jpg
│       ├── camelia-small.jpg
│       └── favicon.svg
```

### Note di compliance

- Privacy Policy e Cookie Policy sono scritte a mano, conformi a GDPR ma non beneficiano della copertura legale di un servizio come iubenda. Per upgrade in seguito (~30€/anno): [iubenda](https://www.iubenda.com/it).
- Il form usa un honeypot anti-spam invisibile (campo `botcheck`). I bot lo riempiono e li scartiamo lato JS.
- Non sono usati cookie di profilazione né analytics: per questo motivo non c'è (e non serve) un cookie banner.
- I font sono caricati da Google Fonts (CDN). Se in futuro vuoi essere 100% privacy-friendly, scarica i font e self-hostali in `assets/fonts/`.

### Roadmap miglioramenti possibili

- [ ] Foto professionale di Emma (shooting con fotografo, ~80-150€)
- [ ] Dominio `.it` (~10€/anno)
- [ ] Email su dominio (`info@emmaveronesi.it` via Cloudflare Routing, gratis)
- [ ] iubenda per privacy/cookie (~30€/anno)
- [ ] Google Search Console + sitemap.xml per SEO
- [ ] Analytics privacy-friendly (Plausible/Umami)
- [ ] Sezione blog/articoli (riprendendo i post Instagram)
- [ ] Calendly o Cal.com integrato per prenotazione diretta
- [ ] Self-hosting dei font Google
