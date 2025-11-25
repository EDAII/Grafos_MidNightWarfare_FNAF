document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    const letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%&";
    document.querySelectorAll('.glitch').forEach(target => {
        let iteration = 0;
        let interval = null;
        
        target.onmouseover = event => {
            iteration = 0;
            clearInterval(interval);
            
            interval = setInterval(() => {
                event.target.innerText = event.target.innerText
                    .split("")
                    .map((letter, index) => {
                        if(index < iteration) {
                            return event.target.dataset.text[index];
                        }
                        return letters[Math.floor(Math.random() * letters.length)];
                    })
                    .join("");
                
                if(iteration >= event.target.dataset.text.length){ 
                    clearInterval(interval);
                }
                
                iteration += 1 / 3;
            }, 30);
        }
    });

    const typeText = document.querySelector('.type-text');
    if(typeText) {
        const text = typeText.innerHTML;
        typeText.innerHTML = '';
        let i = 0;
        function type() {
            if (i < text.length) {
                typeText.innerHTML += text.charAt(i);
                i++;
                setTimeout(type, 20);
            }
        }
        setTimeout(type, 500);
    }

    const observerOptions = {
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    const hiddenElements = document.querySelectorAll('.card, .mechanic-item, .emotion-card, .stat-item, .terminal-window, .requirement-item');
    hiddenElements.forEach((el) => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'all 0.6s cubic-bezier(0.165, 0.84, 0.44, 1)';
        observer.observe(el);
    });
});