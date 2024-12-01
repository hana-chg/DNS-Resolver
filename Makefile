---

# Makefile

```makefile
# Makefile for DNS Resolver

PYTHON = python
SCRIPT = dns_server.py
PIDFILE = server.pid

.PHONY: run clean stop

run:
	@echo "Starting DNS server..."
	@$(PYTHON) $(SCRIPT) & echo $$! > $(PIDFILE)

stop:
	@if [ -f $(PIDFILE) ]; then \
		kill `cat $(PIDFILE)`; \
		rm -f $(PIDFILE); \
		echo "DNS server stopped."; \
	else \
		echo "No running server found."; \
	fi

clean:
	@rm -f $(PIDFILE)
	@echo "Cleaned up temporary files."
```

