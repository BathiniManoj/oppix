document.addEventListener("DOMContentLoaded", function () {

  // Welcome Button
  const buttons = document.querySelectorAll(".btn-primary");

  buttons.forEach(btn => {
    btn.addEventListener("click", function () {
      alert("Welcome to CareerCraft! 🚀");
    });
  });

  // Scroll animation
  const cards = document.querySelectorAll(".card");

  function reveal() {
    cards.forEach(card => {
      const position = card.getBoundingClientRect().top;
      if (position < window.innerHeight - 50) {
        card.style.opacity = "1";
        card.style.transform = "translateY(0)";
      }
    });
  }

  cards.forEach(card => {
    card.style.opacity = "0";
    card.style.transform = "translateY(20px)";
    card.style.transition = "all 0.6s ease";
  });

  window.addEventListener("scroll", reveal);
  reveal();
});

 <!-- JAVASCRIPT -->
  <script>
    function showAlert() {
      alert("Redirecting to Create Free Account page...");
    }

    function showResume() {
      alert("Opening Resume Builder...");
    }
  </script>