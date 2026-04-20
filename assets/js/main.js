/* ============================================================
   Sito Emma Veronesi — JavaScript principale
   - Mobile nav toggle
   - Active link highlighting on scroll
   - Reveal-on-scroll animations
   - Header style on scroll
   - Form submit (Web3Forms) con feedback inline
   - Bottone WhatsApp dinamico da SITE_CONFIG
   ============================================================ */

(function () {
  'use strict';

  /* ---------- Mobile nav ---------- */
  const navToggle = document.querySelector('.nav-toggle');
  const navLinks = document.querySelector('.nav-links');

  if (navToggle && navLinks) {
    navToggle.addEventListener('click', () => {
      const isOpen = navLinks.classList.toggle('open');
      navToggle.classList.toggle('open', isOpen);
      navToggle.setAttribute('aria-expanded', isOpen);
    });

    navLinks.querySelectorAll('a').forEach((link) => {
      link.addEventListener('click', () => {
        navLinks.classList.remove('open');
        navToggle.classList.remove('open');
        navToggle.setAttribute('aria-expanded', 'false');
      });
    });
  }

  /* ---------- Header shadow on scroll ---------- */
  const header = document.querySelector('.site-header');
  if (header) {
    const updateHeader = () => {
      header.classList.toggle('scrolled', window.scrollY > 8);
    };
    updateHeader();
    window.addEventListener('scroll', updateHeader, { passive: true });
  }

  /* ---------- Active section highlighting ---------- */
  const navAnchors = document.querySelectorAll('.nav-links a[href^="#"]');
  const sections = Array.from(navAnchors)
    .map((a) => document.querySelector(a.getAttribute('href')))
    .filter(Boolean);

  if (sections.length && 'IntersectionObserver' in window) {
    const sectionToLink = new Map();
    navAnchors.forEach((a) => {
      const target = document.querySelector(a.getAttribute('href'));
      if (target) sectionToLink.set(target, a);
    });

    const sectionObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            navAnchors.forEach((a) => a.classList.remove('active'));
            const link = sectionToLink.get(entry.target);
            if (link) link.classList.add('active');
          }
        });
      },
      { rootMargin: '-40% 0px -55% 0px', threshold: 0 }
    );

    sections.forEach((s) => sectionObserver.observe(s));
  }

  /* ---------- Reveal on scroll ---------- */
  const reveals = document.querySelectorAll('.reveal');
  if (reveals.length && 'IntersectionObserver' in window) {
    const revealObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            revealObserver.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12 }
    );
    reveals.forEach((el) => revealObserver.observe(el));
  } else {
    reveals.forEach((el) => el.classList.add('visible'));
  }

  /* ---------- WhatsApp button (link dinamico) ---------- */
  const config = window.SITE_CONFIG || {};
  const whatsappBtn = document.querySelector('[data-whatsapp]');
  if (whatsappBtn && config.whatsapp) {
    const numero = config.whatsapp.numero;
    const messaggio = encodeURIComponent(config.whatsapp.messaggio || '');
    whatsappBtn.href = `https://wa.me/${numero}?text=${messaggio}`;
  }

  /* ---------- Form submit (Web3Forms) ---------- */
  const form = document.querySelector('#contatta-form');
  const feedback = document.querySelector('#form-feedback');

  if (form && feedback) {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      feedback.className = 'form-feedback';
      feedback.textContent = '';

      const submitBtn = form.querySelector('button[type="submit"]');
      const originalText = submitBtn.textContent;

      const honeypotField = form.querySelector('input[name="botcheck"]');
      if (honeypotField && honeypotField.value) {
        return;
      }

      const accessKey = config.web3forms?.accessKey;
      const endpoint = config.web3forms?.endpoint || 'https://api.web3forms.com/submit';

      if (!accessKey || accessKey.includes('INSERISCI')) {
        feedback.classList.add('error');
        feedback.textContent =
          'Form non ancora configurato. Per favore scrivi a Emma direttamente via WhatsApp.';
        return;
      }

      submitBtn.disabled = true;
      submitBtn.textContent = 'Invio in corso...';

      try {
        const formData = new FormData(form);
        formData.append('access_key', accessKey);
        formData.append('subject', `Nuovo messaggio dal sito da ${formData.get('name') || 'Anonimo'}`);
        formData.append('from_name', 'Sito Emma Veronesi');

        const res = await fetch(endpoint, {
          method: 'POST',
          body: formData,
        });

        const json = await res.json();

        if (json.success) {
          feedback.classList.add('success');
          feedback.textContent =
            'Grazie per avermi scritto. Ti rispondo personalmente entro 48 ore lavorative.';
          form.reset();
        } else {
          throw new Error(json.message || 'Errore di invio');
        }
      } catch (err) {
        feedback.classList.add('error');
        feedback.textContent =
          'Qualcosa non ha funzionato. Riprova tra qualche minuto, oppure scrivimi via WhatsApp.';
        console.error('Form error:', err);
      } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = originalText;
      }
    });
  }

  /* ---------- Anno corrente nel footer ---------- */
  const yearEl = document.querySelector('[data-year]');
  if (yearEl) {
    yearEl.textContent = new Date().getFullYear();
  }
})();
