# Stage 1 - Build
FROM node:18-alpine AS builder

WORKDIR /app

# Install deps separately (this layer is cached unless package.json changes)
COPY package*.json ./
RUN npm install

# Now copy the source code — this is the only layer that changes most often
COPY . .

# Always clean up stale build
RUN rm -rf .next

# Rebuild app with fresh code
RUN npm run build

# Stage 2 - Runtime
FROM node:18-alpine AS runner

WORKDIR /app

ENV NODE_ENV=production

COPY --from=builder /app/public ./public
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json
COPY --from=builder /app/next.config.ts ./next.config.ts
COPY --from=builder /app/src/questionnaireData ./questionnaireData


EXPOSE 3000
CMD ["npm", "start"]
