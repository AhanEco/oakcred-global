FROM node:20-alpine AS build

WORKDIR /app

COPY frontend/package.json ./

# Install dependencies (ignoring missing lockfile)
RUN npm install

# Copy source
COPY frontend/ ./

# Build the app
RUN npm run build

# Serve with a simple static server
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html

# Expose port
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
