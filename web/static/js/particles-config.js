particlesJS("particles-js", {
  particles: {
    number: {
      value: 70,
      density: { enable: true, value_area: 900 }
    },
    color: { value: ["#7b68ee", "#4d5bce", "#9370db"] },
    shape: {
      type: "circle",
      stroke: { width: 0, color: "#000000" },
      polygon: { nb_sides: 5 }
    },
    opacity: {
      value: 0.4,
      random: true,
      anim: { enable: false }
    },
    size: {
      value: 3,
      random: true,
      anim: { enable: false }
    },
    line_linked: {
      enable: true,
      distance: 150,
      color: "#7b68ee",
      opacity: 0.3,
      width: 1
    },
    move: {
      enable: true,
      speed: 1.2,
      direction: "none",
      random: true,
      straight: false,
      out_mode: "out",
      bounce: false,
      attract: { enable: false, rotateX: 600, rotateY: 1200 }
    }
  },
  interactivity: {
    detect_on: "canvas",
    events: {
      onhover: { enable: true, mode: "repulse" },
      onclick: { enable: true, mode: "push" },
      resize: true
    },
    modes: {
      repulse: { distance: 100, duration: 0.4 },
      push: { particles_nb: 4 },
      bubble: { distance: 400, size: 4, duration: 2, opacity: 0.8, speed: 3 }
    }
  },
  retina_detect: true
});
