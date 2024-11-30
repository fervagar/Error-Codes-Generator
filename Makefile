CC := gcc

CFLAGS := -Wall -O2 -fPIC -fPIE -pie -Wl,-z,now -I.

# Source Files
SRC := example.c error_codes.c

# Generated Header
HEADER := error_codes.h

# YAML Configuration
YAML := error_codes.yml

# Parser Script
PARSER := $(abspath .)/parser.py

TARGET := example

# Default Target
all: $(TARGET)

# Rule to build the target executable
$(TARGET): $(SRC) $(HEADER)
	$(CC) $(CFLAGS) $(SRC) -o $@ $(LDFLAGS)

# Rule to generate error_codes.h
$(HEADER): $(YAML) $(PARSER)
	@echo "Generating $(HEADER) from $(YAML)..."
	$(PARSER) $(YAML) -o $(HEADER)

clean:
	rm -f $(TARGET)

distclean: clean
	rm -f $(HEADER)

.PHONY: all clean distclean
