# Frontend Dockerfile for Vacation Planner
# This is a multi-stage build setup for the SvelteKit app.

# Build stage
FROM node:18-alpine AS build

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy all frontend files
COPY . .

# Build the app
RUN npm run build

# Production stage
FROM node:18-alpine AS production

# Set working directory
WORKDIR /app

# Copy built assets from build stage
COPY --from=build /app/build ./build
COPY --from=build /app/package.json ./package.json

# Install only production dependencies
RUN npm ci --production

# Expose port 3000
EXPOSE 3000

# Command to run the app
CMD ["node", "build"]

# Notes:
# - This assumes you're using SvelteKit with the default build output
# - Adjust the build and run commands if you're using a different configuration
# - For production, consider adding health checks and a non-root user 