FROM node:22.7.0-alpine
WORKDIR /app
COPY . .
ENV API_URL="http://localhost:8000"
ENV WEB_APP_PORT="3000"


RUN apk --no-cache add curl && npm install --production && npm run build

EXPOSE $WEB_APP_PORT

CMD ["npm", "start"]