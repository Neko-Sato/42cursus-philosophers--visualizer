NAME	= libphilovisual.so
SORCS 	= philo_visualizer.c
IDFLAGS	= -I.

$(NAME): $(SORCS)
	$(CC) $(IDFLAGS) -shared -fPIC -o $@ $^

.PHONY: all clean re

all: $(NAME)

clean: 
	$(RM) $(NAME)

re: clean all