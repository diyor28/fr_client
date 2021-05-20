FROM node:12.18.2-alpine3.9 as build-stage
WORKDIR /app
COPY package.json ./
COPY package-lock.json ./

RUN npm install
RUN npm install @vue/cli

COPY . .

CMD NODE_OPTIONS=--max_old_space_size=4096 npm run serve
