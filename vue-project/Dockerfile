# Stage 1: Budowanie aplikacji przy użyciu Node i Vite
FROM node:18-alpine AS builder
WORKDIR /app

# Kopiujemy pliki package.json i package-lock.json (lub yarn.lock)
COPY package*.json ./

# Instalujemy zależności
RUN npm install

# Kopiujemy resztę plików aplikacji
COPY . .

# Budujemy aplikację (Vite utworzy folder 'dist')
RUN npm run build

# Stage 2: Serwowanie aplikacji przy użyciu Nginx
FROM nginx:stable-alpine

# Kopiujemy zbudowaną aplikację do katalogu, który Nginx domyślnie serwuje
COPY --from=builder /app/dist /usr/share/nginx/html

# Opcjonalnie: jeśli korzystasz z trybu history (Vue Router) utwórz własny plik konfiguracji Nginx
# COPY nginx.conf /etc/nginx/conf.d/default.conf

# Otwieramy port 80
EXPOSE 80

# Uruchamiamy Nginx w trybie pierwszego planu
CMD ["nginx", "-g", "daemon off;"]
