BINARY = bin/user-activation

$(BINARY): main.go models/sensor.go go.mod
	go build -o $(BINARY) .

.PHONY: lint
lint:
	go vet ./...

.PHONY: test
test:
	go test ./...

.PHONY: module
module: $(BINARY)
	tar czf module.tar.gz $(BINARY) meta.json

.PHONY: clean
clean:
	rm -rf bin module.tar.gz
