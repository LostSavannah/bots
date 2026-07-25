FROM alpine:latest AS build

WORKDIR /app

RUN apk update
RUN apk upgrade
RUN apk add alpine-sdk linux-headers git zlib-dev openssl-dev gperf cmake
RUN git clone --recursive https://github.com/tdlib/telegram-bot-api.git
WORKDIR /app/telegram-bot-api/build
RUN cmake -DCMAKE_BUILD_TYPE=Release ..
RUN cmake --build . --target install
#RUN cd ../..
#RUN ls -l telegram-bot-api/bin/telegram-bot-api*

FROM alpine:latest

WORKDIR /app
COPY --from=build /app/telegram-bot-api/bin .
ENTRYPOINT [ "/bin/sh" ]
