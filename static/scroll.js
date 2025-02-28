document.addEventListener("DOMContentLoaded", function () {
    const sections = document.querySelectorAll(".section");
    const options = {
        threshold: 0.1
    };
    const observer = new IntersectionObserver(function (entries, observer) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add("show");
                observer.unobserve(entry.target);
            }
        });
    }, options);
    sections.forEach(section => {
        observer.observe(section);
    });
});