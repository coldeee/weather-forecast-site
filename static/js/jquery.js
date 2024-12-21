$(document).ready(function() {
    // Счетчик промежуточных точек
    let waypointCount = 0;
    // Максимальное количество разрешенных промежуточных точек
    const maxWaypoints = 3;

    // Обработчик нажатия на кнопку добавления точки
    $('#add-waypoint').click(function() {
        if (waypointCount < maxWaypoints) {
            waypointCount++;
            // HTML-шаблон для новой промежуточной точки
            const newWaypoint = `
                <div class="form-group waypoint">
                    <label for="waypoint_${waypointCount}">Промежуточная точка ${waypointCount}:</label>
                    <div class="waypoint-container">
                        <input type="text" id="waypoint_${waypointCount}" name="locations[]" required>
                        <button type="button" class="remove-waypoint">×</button>
                    </div>
                </div>
            `;
            // Добавление новой точки в контейнер
            $('#waypoints').append(newWaypoint);
        }
        
        // Отключение кнопки добавления при достижении максимума точек
        if (waypointCount >= maxWaypoints) {
            $('#add-waypoint').prop('disabled', true);
        }
    });

    // Обработчик удаления промежуточной точки
    $(document).on('click', '.remove-waypoint', function() {
        // Удаление контейнера точки
        $(this).closest('.waypoint').remove();
        // Уменьшение счетчика
        waypointCount--;
        // Активация кнопки добавления
        $('#add-waypoint').prop('disabled', false);
    });
});