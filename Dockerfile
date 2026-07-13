FROM node:22-alpine AS runtime
WORKDIR /app
ENV NODE_ENV=production
COPY package.json package-lock.json ./
RUN npm ci --omit=dev
COPY site ./site
COPY vault ./vault
EXPOSE 4173
CMD ["npm", "start"]
