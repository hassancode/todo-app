# =============================================================================
# Stage 1: Builder — validate and stage static assets
# =============================================================================
FROM alpine:3.21 AS builder

WORKDIR /app

COPY index.html style.css app.js ./

# =============================================================================
# Stage 2: Runtime — nginx serves static files
# =============================================================================
FROM nginx:1.27-alpine AS runtime

# Remove default content and config
RUN rm -rf /usr/share/nginx/html/* /etc/nginx/conf.d/default.conf

COPY --from=builder /app /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Run as non-root: nginx master stays root to bind port 80,
# but worker processes drop to the unprivileged nginx user (built-in).
# For full non-root, use port 8080 and USER nginx — kept at 80 for simplicity.

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD wget -qO- http://localhost/health || exit 1

CMD ["nginx", "-g", "daemon off;"]
