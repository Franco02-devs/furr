const menubar = document.querySelector('#menu');
const navbar = document.querySelector('.navbar');
const dropdowns = document.querySelectorAll('.dropdown');

menubar.addEventListener('click', () => {
    navbar.classList.toggle('active');
});

dropdowns.forEach(dropdown => {
    dropdown.addEventListener('mouseover', () => {
        const menu = dropdown.querySelector('.dropdown-menu');
        menu.style.display = 'block';
    });
    
    dropdown.addEventListener('mouseout', () => {
        const menu = dropdown.querySelector('.dropdown-menu');
        menu.style.display = 'none';
    });
});
