<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Получаем данные из POST запроса
    $userData = json_decode(file_get_contents('php://input'), true);

    // Загружаем текущий массив пользователей из файла
    $usersFile = 'users.json';
    $usersData = json_decode(file_get_contents($usersFile), true);

    // Ищем пользователя по user_id и обновляем его данные
    foreach ($usersData as &$user) {
        if ($user['user_id'] === $userData['user_id']) {
            $user = $userData;
            break;
        }
    }

    // Сохраняем обновленные данные обратно в файл
    file_put_contents($usersFile, json_encode($usersData, JSON_PRETTY_PRINT));
}
?>
