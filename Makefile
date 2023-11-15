CXX = g++ -std=c++11
CXXFLAGS =  -Iinclude# -Wall -I/opt/homebrew/include
LDFLAGS = ""# -L/opt/homebrew/lib -lglut -framework OpenGL

# Source and object directories
SRCDIR = src
OBJDIR = obj

# Find all .cpp files in src/ and its subdirectories
SOURCES = $(shell find $(SRCDIR)/ -name '*.cpp')

# Object files with path in obj/ directory
OBJECTS = $(patsubst $(SRCDIR)/%.cpp,$(OBJDIR)/%.o,$(SOURCES))

# Name of the executable
TARGET = cs_game

# Default target
all: $(TARGET)

# Linking the executable from the object files
$(TARGET): $(OBJECTS)
	$(CXX) $(CXXFLAGS) $^ -o $@

# Compiling source files into object files
$(OBJDIR)/%.o: $(SRCDIR)/%.cpp
	@mkdir -p $(@D)
	$(CXX) $(CXXFLAGS) -c $< -o $@

# Clean up
clean:
	rm -rf $(OBJDIR)/*
	rm -f $(TARGET)

.PHONY: all clean
