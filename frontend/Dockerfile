# Используем официальный легковесный образ Node.js
FROM node:18-alpine

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы package.json и package-lock.json для установки зависимостей
COPY package.json package-lock.json ./

# Устанавливаем зависимости и глобально устанавливаем сервер для обслуживания статики
RUN npm install && npm install -g serve && npm cache clean --force

# Копируем остальные файлы проекта
COPY . .

# Устанавливаем переменную окружения для Node.js
ENV NODE_OPTIONS=--openssl-legacy-provider

# Создаем сборку фронтенда
RUN npm run build

# Экспонируем порт, на котором будет запущен сервер
EXPOSE 3000

# Команда для запуска сервера и обслуживания статики
CMD ["serve", "-s", "build", "-l", "3000"]
