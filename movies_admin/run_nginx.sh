#!/bin/bash

TEMPLATE_FILE="/etc/nginx/templates/django.conf.template"
TEMP_CONF_FILE="/etc/nginx/conf.d/django.conf"

# Проверка наличия шаблона
if [[ ! -f "${TEMPLATE_FILE}" ]]; then
    echo "Ошибка: Файл шаблона ${TEMPLATE_FILE} не найден."
    exit 1
fi

# Генерация конфигурации Nginx
echo "Генерация конфигурации Nginx..."
envsubst '$CONTAINER_NAME $PORT' < "${TEMPLATE_FILE}" > "${TEMP_CONF_FILE}"

# Проверка успешности генерации
if [[ ! -f "${TEMP_CONF_FILE}" ]]; then
    echo "Ошибка: Не удалось создать файл ${TEMP_CONF_FILE}."
    exit 1
fi

echo "Сгенерированный файл конфигурации:"
cat "${TEMP_CONF_FILE}"

# Запуск Nginx
echo "Запуск Nginx..."
nginx -g "daemon off;"
