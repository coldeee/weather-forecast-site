document.addEventListener('DOMContentLoaded', function() {
    const canvas = document.getElementById('backgroundCanvas');
    if (!canvas) {
        console.error('Canvas element not found');
        return;
    }

    const ctx = canvas.getContext('2d');
    
    // Установка размеров canvas
    function resizeCanvas() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }
    
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);

    // Массив для хранения точек
    const dots = [];
    const maxDots = 100; // Максимальное количество точек на экране
    const maxDistance = 100; // Максимальное расстояние для соединения двух точек

    // Добавляем объект для хранения позиции мыши
    const mouse = {
        x: canvas.width / 2,
        y: canvas.height / 2
    };

    // Добавляем слушатель событий мыши
    canvas.addEventListener('mousemove', (e) => {
        mouse.x = e.clientX;
        mouse.y = e.clientY;
    });

    // Конструктор для создания новой точки с случайными координатами и скоростью
    function Dot() {
        this.x = Math.random() * canvas.width; // Случайная позиция по оси X
        this.y = Math.random() * canvas.height; // Случайная позиция по оси Y
        this.vx = (Math.random() - 0.5) * 0.5; // Случайная скорость по оси X
        this.vy = (Math.random() - 0.5) * 0.5; // Случайная скорость по оси Y
    }

    // Метод для обновления позиции точки и отражения при достижении границ канваса
    Dot.prototype.update = function() {
        this.x += this.vx; // Обновление позиции по оси X
        this.y += this.vy; // Обновление позиции по оси Y

        // Проверка и отражение от левой и правой границ
        if (this.x < 0 || this.x > canvas.width) this.vx *= -1;
        // Проверка и отражение от верхней и нижней границ
        if (this.y < 0 || this.y > canvas.height) this.vy *= -1;
    };

    // Функция для инициализации массива точек
    function initDots() {
        for (let i = 0; i < maxDots; i++) {
            dots.push(new Dot()); // Добавление новой точки в массив
        }
    }

    // Функция для отрисовки точек и линий между близко расположенными точками
    function drawDots() {
        ctx.clearRect(0, 0, canvas.width, canvas.height); // Очистка канваса перед перерисовкой
        ctx.fillStyle = 'rgba(255, 255, 255, 0.7)'; // Установка цвета заливки для точек
        dots.forEach(dot => {
            ctx.beginPath();
            ctx.arc(dot.x, dot.y, 2, 0, Math.PI * 2); // Рисование круга для точки
            ctx.fill(); // Заливка точки
            
            // Добавляем проверку расстояния до курсора
            const dx = dot.x - mouse.x;
            const dy = dot.y - mouse.y;
            const distance = Math.sqrt(dx * dx + dy * dy);
            
            if (distance < maxDistance) {
                ctx.beginPath();
                ctx.moveTo(dot.x, dot.y);
                ctx.lineTo(mouse.x, mouse.y);
                ctx.stroke();
            }
        });

        // Установка стиля для линий между точками
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.1)';
        ctx.lineWidth = 1; // Толщина линий

        // Проход по всем парам точек для рисования линий между близкими точками
        for (let i = 0; i < dots.length; i++) {
            for (let j = i + 1; j < dots.length; j++) {
                const dx = dots[i].x - dots[j].x; // Разница по оси X
                const dy = dots[i].y - dots[j].y; // Разница по оси Y
                const distance = Math.sqrt(dx * dx + dy * dy); // Расчет расстояния между точками
                if (distance < maxDistance) { // Проверка, находится ли пара точек в пределах максимального расстояния
                    ctx.beginPath();
                    ctx.moveTo(dots[i].x, dots[i].y); // Начало линии у первой точки
                    ctx.lineTo(dots[j].x, dots[j].y); // Конец линии у второй точки
                    ctx.stroke(); // Отрисовка линии
                }
            }
        }
    }

    // Функция для анимации точек и обновления их позиций
    function animate() {
        dots.forEach(dot => dot.update()); // Обновление позиции каждой точки
        drawDots(); // Отрисовка точек и линий
        requestAnimationFrame(animate); // Запрос на следующий кадр анимации
    }

    // Запуск инициализации точек и начала анимации
    initDots();
    animate(); 
}); 