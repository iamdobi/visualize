# Animation Reference — Motion (Framer Motion for Vanilla JS)

## CDN Setup

```html
<script src="https://cdn.jsdelivr.net/npm/motion@12/dist/motion.js"></script>
```

This exposes the global `Motion` object with `animate`, `scroll`, `inView`, `stagger`, `spring`, and more.

## Core API

### `Motion.animate(target, keyframes, options)`
Animate any DOM element(s) with spring physics, easing, and timeline control.

```javascript
// Fade in + slide up
Motion.animate('.card', 
  { opacity: [0, 1], y: [40, 0] },
  { duration: 0.6, ease: 'ease-out' }
);

// Spring physics (bouncy, organic feel)
Motion.animate('.hero-title',
  { opacity: [0, 1], scale: [0.9, 1] },
  { duration: 0.8, ease: Motion.spring({ stiffness: 200, damping: 20 }) }
);

// Staggered children
Motion.animate('.card',
  { opacity: [0, 1], y: [30, 0] },
  { delay: Motion.stagger(0.1), duration: 0.5, ease: 'ease-out' }
);
```

### `Motion.inView(target, callback, options)`
Trigger animations when elements enter the viewport. Better than raw IntersectionObserver.

```javascript
// Animate cards as they scroll into view
Motion.inView('.timeline-card', (info) => {
  Motion.animate(info.target, 
    { opacity: [0, 1], x: [info.target.classList.contains('left') ? -60 : 60, 0] },
    { duration: 0.6, ease: Motion.spring({ stiffness: 150, damping: 18 }) }
  );
}, { amount: 0.3 }); // trigger when 30% visible
```

**CRITICAL:** When using `inView`, elements must have `opacity: 1` as their CSS default. Set `opacity: 0` only via JS right before attaching the observer. This ensures content is visible if JS fails or for print/screenshot.

```javascript
// CORRECT pattern: hide via JS, not CSS
document.querySelectorAll('.animate-on-scroll').forEach(el => {
  el.style.opacity = '0';
  el.style.transform = 'translateY(30px)';
});
Motion.inView('.animate-on-scroll', (info) => {
  Motion.animate(info.target,
    { opacity: 1, y: 0 },
    { duration: 0.5, ease: 'ease-out' }
  );
}, { amount: 0.2 });
```

### `Motion.scroll(callback, options)`
Link animations to scroll progress.

```javascript
// Progress bar based on scroll position
Motion.scroll(
  Motion.animate('.progress-bar', { scaleX: [0, 1] }),
  { target: document.querySelector('.content') }
);

// Parallax effect
Motion.scroll(
  Motion.animate('.hero-bg', { y: [0, -100] }),
  { offset: ['start start', 'end start'] }
);
```

### `Motion.spring()`
Spring physics for natural, organic motion.

```javascript
// Gentle spring (smooth, professional)
Motion.spring({ stiffness: 150, damping: 20 })

// Bouncy spring (playful, attention-grabbing)
Motion.spring({ stiffness: 300, damping: 15 })

// Stiff spring (snappy, responsive)
Motion.spring({ stiffness: 400, damping: 30 })
```

### `Motion.stagger(duration, options)`
Stagger animations across multiple elements.

```javascript
// Simple stagger (100ms between each)
Motion.stagger(0.1)

// Stagger from center outward
Motion.stagger(0.1, { from: 'center' })

// Stagger from last element
Motion.stagger(0.1, { from: 'last' })
```

## Animation Recipes

### Hero Entrance (Title + Subtitle + CTA)
```javascript
// Orchestrated hero entrance with spring physics
Motion.animate('.hero-title',
  { opacity: [0, 1], y: [50, 0] },
  { duration: 0.8, ease: Motion.spring({ stiffness: 150, damping: 18 }) }
);
Motion.animate('.hero-subtitle',
  { opacity: [0, 1], y: [30, 0] },
  { delay: 0.2, duration: 0.6, ease: 'ease-out' }
);
Motion.animate('.hero-cta',
  { opacity: [0, 1], y: [20, 0], scale: [0.95, 1] },
  { delay: 0.4, duration: 0.5, ease: Motion.spring({ stiffness: 200, damping: 20 }) }
);
```

### Card Grid Entrance (Staggered)
```javascript
Motion.animate('.card',
  { opacity: [0, 1], y: [40, 0], scale: [0.95, 1] },
  { delay: Motion.stagger(0.08), duration: 0.5, ease: Motion.spring({ stiffness: 200, damping: 22 }) }
);
```

### Stat Counter Animation
```javascript
function animateCounter(el, target, duration = 1.5) {
  const obj = { val: 0 };
  Motion.animate(obj, { val: target }, {
    duration,
    ease: 'ease-out',
    onUpdate: () => {
      el.textContent = Math.round(obj.val).toLocaleString();
    }
  });
}

// Trigger on scroll into view
Motion.inView('.stat-number', (info) => {
  const target = parseInt(info.target.dataset.value);
  animateCounter(info.target, target);
}, { amount: 0.5 });
```

### Chart Reveal
```javascript
// Fade in chart container + scale up
Motion.inView('.chart-container', (info) => {
  Motion.animate(info.target,
    { opacity: [0, 1], scale: [0.9, 1] },
    { duration: 0.6, ease: Motion.spring({ stiffness: 150, damping: 20 }) }
  );
});
```

### Slide Transitions (for decks)
```javascript
function transitionSlide(outEl, inEl, direction = 1) {
  // Exit current slide
  Motion.animate(outEl,
    { opacity: [1, 0], x: [0, -100 * direction] },
    { duration: 0.4, ease: 'ease-in' }
  ).finished.then(() => outEl.style.display = 'none');
  
  // Enter next slide
  inEl.style.display = 'flex';
  Motion.animate(inEl,
    { opacity: [0, 1], x: [100 * direction, 0] },
    { duration: 0.4, ease: Motion.spring({ stiffness: 200, damping: 25 }) }
  );
}
```

### Timeline Scroll Reveal
```javascript
// Progressive reveal with alternating directions
document.querySelectorAll('.timeline-item').forEach((item, i) => {
  item.style.opacity = '0';
  const fromLeft = item.classList.contains('left');
  item.style.transform = `translateX(${fromLeft ? '-60px' : '60px'})`;
});

Motion.inView('.timeline-item', (info) => {
  const fromLeft = info.target.classList.contains('left');
  Motion.animate(info.target,
    { opacity: 1, x: 0 },
    { duration: 0.6, ease: Motion.spring({ stiffness: 120, damping: 18 }) }
  );
}, { amount: 0.2 });
```

### Hover Micro-interactions
```javascript
document.querySelectorAll('.card').forEach(card => {
  card.addEventListener('mouseenter', () => {
    Motion.animate(card, { scale: 1.02, y: -4 }, { duration: 0.2 });
  });
  card.addEventListener('mouseleave', () => {
    Motion.animate(card, { scale: 1, y: 0 }, { duration: 0.3 });
  });
});
```

### Number Ticker (for KPIs/dashboards)
```javascript
Motion.inView('.kpi-value', (info) => {
  const el = info.target;
  const target = parseFloat(el.dataset.value);
  const prefix = el.dataset.prefix || '';
  const suffix = el.dataset.suffix || '';
  const decimals = el.dataset.decimals || 0;
  
  Motion.animate({ val: 0 }, { val: target }, {
    duration: 1.2,
    ease: [0.25, 0.46, 0.45, 0.94],
    onUpdate: (latest) => {
      el.textContent = prefix + latest.val.toFixed(decimals) + suffix;
    }
  });
});
```

### Morphing Progress Ring
```javascript
function animateRing(el, percent) {
  const circumference = 2 * Math.PI * 45; // r=45
  Motion.animate(el,
    { strokeDashoffset: [circumference, circumference * (1 - percent / 100)] },
    { duration: 1.5, ease: Motion.spring({ stiffness: 100, damping: 20 }) }
  );
}
```

## When to Use Motion vs CSS

| Animation Type | Use Motion | Use CSS |
|---|---|---|
| Entrance animations | ✅ Spring physics feel better | ⚠️ OK for simple fades |
| Scroll-triggered | ✅ `inView` is cleaner than IntersectionObserver | ❌ No CSS-only solution |
| Hover effects | ✅ Spring-based scale/lift | ✅ Simple transitions fine |
| Staggered reveals | ✅ `stagger()` is perfect | ⚠️ Needs manual `animation-delay` |
| Number counters | ✅ Only way to do this | ❌ Not possible in CSS |
| Slide transitions | ✅ Spring physics + orchestration | ⚠️ Basic transitions only |
| Loading spinners | ❌ Overkill | ✅ `@keyframes` is fine |
| Theme transitions | ❌ CSS handles this | ✅ `transition: all 0.3s` |

## Reduced Motion

**ALWAYS respect user preferences:**

```javascript
// Check before running animations
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

if (!prefersReducedMotion) {
  // Run Motion animations
  Motion.animate('.card', { opacity: [0, 1], y: [30, 0] }, { delay: Motion.stagger(0.1) });
} else {
  // Just show everything immediately
  document.querySelectorAll('.card').forEach(el => {
    el.style.opacity = '1';
    el.style.transform = 'none';
  });
}
```

## Performance Tips

- Motion uses the Web Animations API (WAAPI) under the hood — hardware accelerated
- Prefer animating `opacity`, `transform`, `scale`, `x`, `y`, `rotate` (compositor-only)
- Avoid animating `width`, `height`, `top`, `left`, `margin`, `padding` (trigger layout)
- For many elements (50+), batch animations or use `will-change: transform`
- CDN size: ~15KB gzipped — lightweight enough for single-file HTML
