document.addEventListener('DOMContentLoaded', () => {
  
  /* ==========================================
     1. ТЕМЫ ОФОРМЛЕНИЯ (DARK/LIGHT THEME)
     ========================================== */
  const themeToggleBtn = document.getElementById('theme-toggle');
  const savedTheme = localStorage.getItem('theme');
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  
  if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
    document.body.classList.add('dark-theme');
  } else {
    document.body.classList.remove('dark-theme');
  }

  themeToggleBtn.addEventListener('click', () => {
    document.body.classList.toggle('dark-theme');
    const currentTheme = document.body.classList.contains('dark-theme') ? 'dark' : 'light';
    localStorage.setItem('theme', currentTheme);
  });

  /* ==========================================
     1B. ПЕРЕКЛЮЧЕНИЕ ЯЗЫКОВ (LANGUAGE SWITCHER)
     ========================================== */
  const langSelector = document.getElementById('lang-selector');
  const langBtn = document.getElementById('lang-btn');
  const langDropdownItems = document.querySelectorAll('.lang-dropdown-item');

  // Load default language (always English on open)
  if (window.applyTranslations) {
    window.applyTranslations('en');
  }

  if (langBtn && langSelector) {
    // Toggle dropdown
    langBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      langSelector.classList.toggle('active');
    });

    // Close dropdown on click outside
    document.addEventListener('click', (e) => {
      if (!langSelector.contains(e.target)) {
        langSelector.classList.remove('active');
      }
    });

    // Language selection
    langDropdownItems.forEach(item => {
      item.addEventListener('click', () => {
        const lang = item.getAttribute('data-lang');
        if (window.applyTranslations) {
          window.applyTranslations(lang);
        }
        langSelector.classList.remove('active');
      });
    });
  }

  /* ==========================================
     6. БОКОВОЙ ВИДЖЕТ НАВИГАЦИИ (SIDE NAV WIDGET)
     ========================================== */
  const sideNavList = document.getElementById('side-nav-list');
  const sideNavWidget = document.getElementById('side-nav-widget');
  let isProgrammaticScroll = false;
  let programmaticScrollTimer = null;

  function setActiveNavItem(id) {
    const navItems = document.querySelectorAll('.side-nav-item');
    navItems.forEach(item => {
      if (item.getAttribute('data-target') === id) {
        item.classList.add('active');
        if (window.innerWidth <= 900 && sideNavList) {
          const listWidth = sideNavList.clientWidth;
          const itemLeft = item.offsetLeft;
          const itemWidth = item.offsetWidth;
          sideNavList.scrollTo({
            left: itemLeft - (listWidth / 2) + (itemWidth / 2),
            behavior: 'smooth'
          });
        }
      } else {
        item.classList.remove('active');
      }
    });
  }

  function handleScrollSpy() {
    if (isProgrammaticScroll) return;

    const activePanel = document.querySelector('.tab-panel.active');
    if (!activePanel) return;

    const sections = Array.from(activePanel.querySelectorAll('.about-section[id]'));
    if (sections.length === 0) return;

    const scrollY = window.pageYOffset || document.documentElement.scrollTop;
    const viewportHeight = window.innerHeight;
    const pageHeight = document.documentElement.scrollHeight;

    // 1. If at/near top of page, always highlight first section
    if (scrollY < 50) {
      setActiveNavItem(sections[0].id);
      return;
    }

    // 2. If reached bottom of page on a scrollable page, highlight last section
    if (pageHeight > viewportHeight + 100 && scrollY + viewportHeight >= pageHeight - 50) {
      setActiveNavItem(sections[sections.length - 1].id);
      return;
    }

    // 3. Offset line for active section detection (140px below viewport top)
    const offsetCheck = scrollY + 140;
    let currentSectionId = sections[0].id;

    for (let i = 0; i < sections.length; i++) {
      const sec = sections[i];
      const secTop = sec.getBoundingClientRect().top + scrollY;
      if (secTop <= offsetCheck) {
        currentSectionId = sec.id;
      } else {
        break;
      }
    }

    setActiveNavItem(currentSectionId);
  }

  window.addEventListener('scroll', handleScrollSpy, { passive: true });

  /* ==========================================
     2. ПЕРЕКЛЮЧЕНИЕ ВКЛАДОК (TAB SWITCHING)
     ========================================== */
  const tabBtns = document.querySelectorAll('.tab-btn');
  const tabPanels = document.querySelectorAll('.tab-panel');

  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      tabBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      const targetTabId = btn.getAttribute('data-tab');

      tabPanels.forEach(panel => {
        panel.classList.remove('active');
      });

      const activePanel = document.getElementById(targetTabId);
      if (activePanel) {
        activePanel.classList.add('active');
      }
      isProgrammaticScroll = false;
      if (window.updateSideNav) {
        window.updateSideNav();
      }
      handleScrollSpy();
    });
  });

  /* ==========================================
     3. КОПИРОВАНИЕ РЕКВИЗИТОВ (COPY TO CLIPBOARD)
     ========================================== */
  const copyButtons = document.querySelectorAll('.btn-copy');
  copyButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const textToCopy = btn.getAttribute('data-copy');
      navigator.clipboard.writeText(textToCopy).then(() => {
        const copiedText = btn.getAttribute('data-translated-copied') || 'Copied! ✓';
        const copyText = btn.getAttribute('data-translated-copy') || 'Copy';
        btn.textContent = copiedText;
        btn.classList.add('copied');
        setTimeout(() => {
          btn.textContent = copyText;
          btn.classList.remove('copied');
        }, 2000);
      }).catch(err => {
        console.error('Не удалось скопировать текст: ', err);
      });
    });
  });

  /* ==========================================
     4. АВТОРИЗАЦИЯ ДЛЯ ПУПУНЬКИ (SECRET AUTH)
     ========================================== */
  // Авторизация перенесена в secret.html для предотвращения двойного ввода пароля.

  /* ==========================================
     5. РАСКРЫТИЕ/ЗАКРЫТИЕ ВИШЛИСТА (WISHLIST ACCORDION)
     ========================================== */
  const wishlistCard = document.querySelector('.wishlist-card-collapsible');
  const wishlistToggle = document.querySelector('.wishlist-toggle-header');

  if (wishlistCard && wishlistToggle) {
    wishlistToggle.addEventListener('click', () => {
      wishlistCard.classList.toggle('collapsed');
    });
  }



  window.updateSideNav = function() {
    if (!sideNavList) return;
    sideNavList.innerHTML = '';

    const activePanel = document.querySelector('.tab-panel.active');
    if (!activePanel) return;

    const sections = activePanel.querySelectorAll('.about-section[id]');
    if (sections.length === 0) {
      if (sideNavWidget) sideNavWidget.style.display = 'none';
      return;
    } else {
      if (sideNavWidget) sideNavWidget.style.display = '';
    }

    sections.forEach((sec, idx) => {
      const titleEl = sec.querySelector('.section-title');
      if (!titleEl) return;

      let titleText = '';
      const i18nKey = titleEl.getAttribute('data-i18n');
      if (i18nKey) {
        titleText = titleEl.textContent.trim();
      } else {
        const childSpan = titleEl.querySelector('span[data-i18n]');
        if (childSpan) {
          titleText = childSpan.textContent.trim();
        } else {
          titleText = titleEl.childNodes[0]?.textContent?.trim() || titleEl.textContent.trim();
        }
      }

      const a = document.createElement('a');
      a.href = '#' + sec.id;
      a.className = 'side-nav-item';
      a.setAttribute('data-target', sec.id);
      if (idx === 0) a.classList.add('active');

      const spanText = document.createElement('span');
      spanText.className = 'side-nav-text';
      spanText.textContent = titleText;

      a.appendChild(spanText);

      a.addEventListener('click', (e) => {
        e.preventDefault();
        const targetSec = document.getElementById(sec.id);
        if (targetSec) {
          isProgrammaticScroll = true;
          if (programmaticScrollTimer) clearTimeout(programmaticScrollTimer);

          setActiveNavItem(sec.id);

          const headerOffset = 25;
          const elementPosition = targetSec.getBoundingClientRect().top;
          const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

          window.scrollTo({
            top: offsetPosition,
            behavior: 'smooth'
          });

          programmaticScrollTimer = setTimeout(() => {
            isProgrammaticScroll = false;
          }, 800);
        }
      });

      sideNavList.appendChild(a);
    });

    handleScrollSpy();
  };

  // Initial side nav setup
  if (window.updateSideNav) {
    window.updateSideNav();
  }
});

