FROM node:latest

# Create app directory
WORKDIR /app

ENV PATH /app/node_modules/.bin:${PATH}

# Install app dependencies
COPY /app/public ./public
COPY /app/src ./src
COPY /app/package*.json ./
RUN npm install

EXPOSE 3000
CMD ["npm", "start"]