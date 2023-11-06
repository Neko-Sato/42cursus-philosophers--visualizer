NAME	= libphilovisual.so
SORCS 	= philo_visualizer.c
IDFLAGS	= -I.

$(NAME): $(SORCS)
	$(CC) $(IDFLAGS) -shared -fPIC -o $@ $^

.PHONY: clean
clean: 
	$(RM) $(NAME)