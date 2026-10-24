(function () {
  const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  const revealNodes = (root) => {
    if (prefersReducedMotion) return;
    const targets = root.querySelectorAll(".reveal:not(.in-view)");
    if (!targets.length) return;

    if (!("IntersectionObserver" in window)) {
      targets.forEach((node) => node.classList.add("in-view"));
      return;
    }

    const observer = new IntersectionObserver(
      (entries, obs) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("in-view");
            obs.unobserve(entry.target);
          }
        });
      },
      {
        root: null,
        threshold: 0.14,
        rootMargin: "0px 0px -40px 0px"
      }
    );

    targets.forEach((node) => observer.observe(node));
  };

  /**
   * Syncs Mermaid blocks, converting any <pre.mermaid> or <pre><code> blocks
   * into clean <div class="mermaid"> containers while preserving the original code
   * in a data-mermaid-code attribute for safe re-rendering on dark/light mode toggles.
   */
  const syncMermaidBlocks = (root) => {
    // 1. Handle superfences pre.mermaid and code.mermaid
    root.querySelectorAll("pre.mermaid, pre code.language-mermaid, pre code.mermaid").forEach((el) => {
      const pre = el.tagName.toLowerCase() === "pre" ? el : el.closest("pre");
      if (!pre) return;

      const codeEl = pre.querySelector("code");
      const rawCode = (codeEl ? codeEl.textContent : pre.textContent) || "";
      if (!rawCode.trim()) return;

      const block = document.createElement("div");
      block.className = "mermaid";
      block.setAttribute("data-mermaid-code", rawCode.trim());
      block.textContent = rawCode.trim();
      pre.replaceWith(block);
    });

    // 2. Cache source code on any existing div.mermaid
    root.querySelectorAll("div.mermaid").forEach((block) => {
      if (!block.getAttribute("data-mermaid-code")) {
        const text = block.textContent.trim();
        if (text && !text.startsWith("<svg")) {
          block.setAttribute("data-mermaid-code", text);
        }
      }
    });
  };

  /**
   * Initializes and renders Mermaid diagrams with theme-appropriate styling
   * for both Dark (slate) and Light (default) palettes.
   */
  const renderMermaid = async (root) => {
    if (typeof window.mermaid === "undefined") return;

    syncMermaidBlocks(root);
    const blocks = root.querySelectorAll(".mermaid");
    if (!blocks.length) return;

    const isDarkMode = document.body.getAttribute("data-md-color-scheme") === "slate";

    window.mermaid.initialize({
      startOnLoad: false,
      securityLevel: "loose",
      theme: isDarkMode ? "dark" : "default",
      themeVariables: isDarkMode
        ? {
            darkMode: true,
            background: "#1E1C19",
            mainBkg: "#262420",
            nodeBorder: "#D97757",
            primaryColor: "#262420",
            primaryBorderColor: "#D97757",
            primaryTextColor: "#F4F3EE",
            secondaryColor: "#1F1E1B",
            tertiaryColor: "#141413",
            lineColor: "#D4A373",
            textColor: "#F4F3EE",
            titleColor: "#F4F3EE",
            fontFamily: "'Inter', -apple-system, sans-serif",
            fontSize: "14px",

            // Flowchart & Nodes
            edgeLabelBackground: "#1E1C19",
            nodeTextColor: "#F4F3EE",
            clusterBkg: "#1B1A17",
            clusterBorder: "#403B35",

            // Sequence Diagram Variables (High Contrast Dark Mode)
            actorBkg: "#262420",
            actorBorder: "#D97757",
            actorTextColor: "#F4F3EE",
            actorLineColor: "#D4A373",
            signalColor: "#F4F3EE",
            signalTextColor: "#F4F3EE",
            labelBoxBkgColor: "#262420",
            labelBoxBorderColor: "#D97757",
            labelTextColor: "#F4F3EE",
            loopTextColor: "#F4F3EE",
            noteBkgColor: "#332A22",
            noteBorderColor: "#D97757",
            noteTextColor: "#F4F3EE",
            activationBorderColor: "#D97757",
            activationBkgColor: "#3D2B22",
            sequenceNumberColor: "#141413",

            // Class & State Diagram
            classText: "#F4F3EE",
            stateBkg: "#262420",
            stateBorder: "#D97757",
            labelColor: "#F4F3EE"
          }
        : {
            darkMode: false,
            background: "#FFFFFF",
            mainBkg: "#FAF9F5",
            nodeBorder: "#D97757",
            primaryColor: "#FAF9F5",
            primaryBorderColor: "#D97757",
            primaryTextColor: "#1C1917",
            secondaryColor: "#F3F2EB",
            tertiaryColor: "#E7E5DC",
            lineColor: "#8A857D",
            textColor: "#1C1917",
            titleColor: "#1C1917",
            fontFamily: "'Inter', -apple-system, sans-serif",
            fontSize: "14px",

            // Flowchart & Nodes
            edgeLabelBackground: "#FFFFFF",
            nodeTextColor: "#1C1917",
            clusterBkg: "#F4F2EB",
            clusterBorder: "#D97757",

            // Sequence Diagram Variables
            actorBkg: "#FAF9F5",
            actorBorder: "#D97757",
            actorTextColor: "#1C1917",
            actorLineColor: "#8A857D",
            signalColor: "#1C1917",
            signalTextColor: "#1C1917",
            labelBoxBkgColor: "#F3F2EB",
            labelBoxBorderColor: "#D97757",
            labelTextColor: "#1C1917",
            loopTextColor: "#1C1917",
            noteBkgColor: "#FFF8F2",
            noteBorderColor: "#D97757",
            noteTextColor: "#1C1917",
            activationBorderColor: "#D97757",
            activationBkgColor: "#F5EBE6",
            sequenceNumberColor: "#FFFFFF"
          },
      flowchart: {
        curve: "basis",
        htmlLabels: true
      }
    });

    // Restore pristine diagram source code before rendering
    blocks.forEach((block) => {
      const src = block.getAttribute("data-mermaid-code");
      if (src) {
        block.textContent = src;
      }
      block.removeAttribute("data-processed");
    });

    await window.mermaid.run({ querySelector: ".mermaid" });
  };

  const initEnhancements = () => {
    revealNodes(document);
    renderMermaid(document).catch((error) => {
      console.warn("Mermaid render failed:", error);
    });
  };

  // Subscribe to Material for MkDocs navigation
  if (typeof document$ !== "undefined") {
    document$.subscribe(initEnhancements);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initEnhancements);
  } else {
    initEnhancements();
  }

  // Live theme switch watcher (Slate <-> Default)
  if (typeof MutationObserver !== "undefined") {
    const observer = new MutationObserver((changes) => {
      const schemeChanged = changes.some(
        (change) =>
          change.type === "attributes" &&
          change.attributeName === "data-md-color-scheme"
      );
      if (schemeChanged) {
        renderMermaid(document).catch((error) => {
          console.warn("Mermaid theme refresh failed:", error);
        });
      }
    });
    observer.observe(document.body, {
      attributes: true,
      attributeFilter: ["data-md-color-scheme"]
    });
  }
})();
