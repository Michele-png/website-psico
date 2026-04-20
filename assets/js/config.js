/* ============================================================
   CONFIGURAZIONE TECNICA — modifica solo Michele
   ============================================================
   Questo file contiene chiavi API e numeri di telefono che NON
   devono finire in mano a Emma per evitare di romperli per sbaglio.

   Quando ottieni la chiave Web3Forms:
   1. Vai su https://web3forms.com/, clicca "Create your Access Key"
   2. Inserisci l'email di Emma (è dove arriveranno i messaggi)
   3. Copia la chiave che riceverai via email
   4. Sostituisci 'INSERISCI-QUI-LA-CHIAVE-WEB3FORMS' qui sotto

   Per il numero WhatsApp: formato internazionale senza '+', es. 393331234567
   ============================================================ */

window.SITE_CONFIG = {
  web3forms: {
    accessKey: 'INSERISCI-QUI-LA-CHIAVE-WEB3FORMS',
    endpoint: 'https://api.web3forms.com/submit',
  },

  whatsapp: {
    numero: '393331234567',
    messaggio: 'Ciao Emma, ti scrivo dal tuo sito perché vorrei...',
  },
};
