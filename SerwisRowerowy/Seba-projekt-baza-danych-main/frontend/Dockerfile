# Use a Node.js base image
FROM node:18-alpine

WORKDIR /app

COPY shop_admin_app/package.json .
COPY shop_admin_app/package-lock.json .

RUN npm install

COPY shop_admin_app/ .

EXPOSE 8000

CMD ["npm", "run", "dev"]