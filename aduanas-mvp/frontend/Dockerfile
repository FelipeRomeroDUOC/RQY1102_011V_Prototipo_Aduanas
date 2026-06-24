FROM node:20-alpine

WORKDIR /app

# Copiar configuración de paquetes
COPY package.json package-lock.json* ./

# Instalar dependencias
RUN npm install

# Copiar el resto del código
COPY . .

# Exponer el puerto de Vite
EXPOSE 5173

# Ejecutar el servidor de desarrollo de Vite (accesible desde fuera del contenedor)
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
