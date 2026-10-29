// Enhanced UX enhancements: Clipboard paste, Intersection scroll spy, mobile result focus
document.addEventListener("DOMContentLoaded", () => {
  // 1. Nav highlight follows scroll (desktop + mobile bars)
  const links = [...document.querySelectorAll(".nav-link, .mobile-nav a")];
  const sections = ["home", "diagnose", "guidance"].map(id => document.getElementById(id)).filter(Boolean);
  if ("IntersectionObserver" in window && sections.length > 0) {
    const spy = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        links.forEach(a => a.classList.toggle("active", a.getAttribute("href") === `#${entry.target.id}`));
      });
    }, { rootMargin: "-30% 0px -55% 0px" });
    sections.forEach(s => spy.observe(s));
  }

  // 2. Paste a leaf photo straight from clipboard (Ctrl + V)
  document.addEventListener("paste", event => {
    const items = event.clipboardData?.items;
    if (!items) return;
    for (let i = 0; i < items.length; i++) {
      if (items[i].type.indexOf("image") !== -1) {
        const file = items[i].getAsFile();
        if (file) {
          const input = document.getElementById("file-input");
          if (input) {
            const dataTransfer = new DataTransfer();
            dataTransfer.items.add(file);
            input.files = dataTransfer.files;
            input.dispatchEvent(new Event("change", { bubbles: true }));
          }
          break;
        }
      }
    }
  });

  // 3. Smoothly scroll to results card on smaller screens when prediction finishes
  const badge = document.getElementById("result-state-badge");
  if (badge) {
    new MutationObserver(() => {
      if (badge.textContent.includes("ready") && window.matchMedia("(max-width: 960px)").matches) {
        document.getElementById("results-card")?.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    }).observe(badge, { childList: true, characterData: true, subtree: true });
  }
});
