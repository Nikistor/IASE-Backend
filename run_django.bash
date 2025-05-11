#!/bin/bash

# Цвета
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # Без цвета

echo -e "${CYAN}▶️  Запуск Django миграций...${NC}"
python3 manage.py migrate
echo -e "${GREEN}✅ Миграции применены успешно!${NC}"
echo ""

echo -e "${CYAN}👤 Добавление пользователей...${NC}"
python3 manage.py add_users
echo -e "${GREEN}✅ Пользователи добавлены!${NC}"
echo ""

echo -e "${CYAN}📦 Заполнение базы данных...${NC}"
python3 manage.py fill_db
echo -e "${GREEN}✅ База данных успешно заполнена!${NC}"
echo ""

echo -e "${YELLOW}⚠️ Обратите внимание: поле companies в модели Requisition использует null, что не влияет на ManyToManyField.${NC}"
