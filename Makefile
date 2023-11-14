CXX = g++ -std=c++11
CXXFLAGS =  ""# -Wall -I/opt/homebrew/include
LDFLAGS = ""# -L/opt/homebrew/lib -lglut -framework OpenGL

# Object files
OBJS = connection.o client.o

# Target executable
TARGET = cs_game

# Build rules
all: $(TARGET)

$(TARGET): $(OBJS)
	$(CXX) -o $@ $^ $(LDFLAGS)

connection.o: connection/connection.cpp connection/connection.h
	$(CXX) $(CXXFLAGS) -c -o $@ $<

client.o: client.cpp
	$(CXX) $(CXXFLAGS) -c -o $@ $<

clean:
	rm -f *.o $(TARGET).exe
