;(() => {
  // Intersection Observer for scroll animations
  const observerOptions = {
    threshold: 0.1,
    rootMargin: "0px 0px -50px 0px",
  }

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("visible")
      }
    })
  }, observerOptions)

  function initScrollAnimations() {
    document.querySelectorAll(".card").forEach((card) => {
      card.classList.add("fade-in-on-scroll")
      observer.observe(card)
    })
  }

  function initProgressBars() {
    document.querySelectorAll(".progress-bar").forEach((bar) => {
      const width = bar.style.width || bar.getAttribute("aria-valuenow") + "%"
      bar.style.width = "0"
      setTimeout(() => {
        bar.style.width = width
      }, 300)
    })
  }

  function initBadgeAnimations() {
    document.querySelectorAll(".habitability-badge").forEach((badge, index) => {
      badge.style.animationDelay = `${index * 0.1}s`
      badge.style.animation = "scaleIn 0.5s ease-out both"
    })
  }

  // Initialize all animations when DOM is ready
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", () => {
      initScrollAnimations()
      initProgressBars()
      initBadgeAnimations()
    })
  } else {
    initScrollAnimations()
    initProgressBars()
    initBadgeAnimations()
  }
})()
