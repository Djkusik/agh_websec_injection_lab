FROM golang:1.15-buster

RUN useradd epilepsy

WORKDIR /go/src/epilepsy

RUN go get github.com/joho/godotenv
COPY static static
COPY templates templates
COPY server.go flag.go .en[v] ./

RUN chown -R epilepsy:epilepsy ./
RUN go install
USER epilepsy

EXPOSE 5001
CMD [ "epilepsy" ]