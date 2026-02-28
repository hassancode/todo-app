FROM nginx:alpine-slim@sha256:a716a2895ddba4fa7fca05e1003579f76d3d304932781426a211bc72b51f0c4e

# Copy static assets and custom nginx config
COPY index.html app.js style.css /usr/share/nginx/html/
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD nc -zw1 localhost 80 || exit 1
