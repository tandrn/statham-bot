#!/usr/bin/env bash
set -euo pipefail

# ============================================
#  Скрипт деплоя бота Стетхема на Yandex Cloud
# ============================================

# === НАСТРОЙКИ (замени на свои!) ===
BOT_TOKEN="YOUR_BOT_TOKEN_HERE"
FUNCTION_NAME="statham-bot"
RUNTIME="python312"
ENTRYPOINT="index.handler"
SOURCE_DIR="./function"

echo "=== Шаг 1: Создание Cloud Function ==="
yc serverless function create \
  --name "${FUNCTION_NAME}" \
  --description "ТГ-бот мемных цитат Джейсона Стетхема" \
  2>/dev/null || echo "Функция уже существует, пропускаем"

echo "=== Шаг 2: Получение ID функции ==="
FUNCTION_ID=$(yc serverless function get "${FUNCTION_NAME}" --format=json | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")
echo "Function ID: ${FUNCTION_ID}"

echo "=== Шаг 3: Деплоя версии функции ==="
yc serverless function version create \
  --function-id "${FUNCTION_ID}" \
  --runtime "${RUNTIME}" \
  --entrypoint "${ENTRYPOINT}" \
  --source-path "${SOURCE_DIR}" \
  --environment "BOT_TOKEN=${BOT_TOKEN}" \
  --execution-timeout 30s

echo "=== Шаг 4: Получение URL функции ==="
FUNCTION_URL=$(yc serverless function get "${FUNCTION_NAME}" --format=json | python3 -c "import sys,json; print(json.load(sys.stdin).get('http_invoke_url',''))")
echo "Function URL: ${FUNCTION_URL}"

echo "=== Шаг 5: Установка Telegram Webhook ==="
WEBHOOK_RESPONSE=$(curl -s "https://api.telegram.org/bot${BOT_TOKEN}/setWebhook?url=${FUNCTION_URL}")
echo "Webhook response: ${WEBHOOK_RESPONSE}"

echo ""
echo "=== ГОТОВО! ==="
echo "Бот развёрнут и webhook установлен."
echo "Открой Telegram и напиши /start своему боту."
echo "URL функции: ${FUNCTION_URL}"
