# Stage 1: Build dependencies in Linux environment
FROM node:20-slim AS deps
WORKDIR /app
COPY package*.json ./
RUN npm install

# Stage 2: Run Vite dev server
FROM node:20-slim
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host"]
