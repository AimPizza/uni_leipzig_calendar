# based on: https://github.com/pavelzw/pixi-docker-example/blob/main/3-multi-stage/Dockerfile
FROM ghcr.io/prefix-dev/pixi:noble AS build

WORKDIR /app
COPY . .
RUN pixi install --locked
RUN pixi shell-hook -s bash > /shell-hook
RUN echo "#!/bin/bash" > /app/entrypoint.sh
RUN cat /shell-hook >> /app/entrypoint.sh
RUN echo 'exec "$@"' >> /app/entrypoint.sh

FROM ubuntu:24.04 AS production
WORKDIR /app
COPY --from=build /app/.pixi/envs/default /app/.pixi/envs/default
COPY --from=build --chmod=0755 /app/entrypoint.sh /app/entrypoint.sh
COPY ./src/uni_leipzig_calendar /app/src/uni_leipzig_calendar

EXPOSE 3000
ENTRYPOINT [ "/app/entrypoint.sh" ]
CMD [ "python", "src/uni_leipzig_calendar/main.py" ]
