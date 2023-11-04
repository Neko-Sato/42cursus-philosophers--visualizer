#include "philo_visualizer.h"
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/un.h>
#include <unistd.h>

static int	sock = -1;

static void	philovisualizer_final(void);

void	philovisualizer_init(void)
{
	struct sockaddr_un	addr;

	sock = socket(AF_LOCAL, SOCK_STREAM, 0);
	if (sock < 0)
		return ;
	addr.sun_family = AF_LOCAL;
	strcpy(addr.sun_path, PV_PATH);
	if (connect(sock, (struct sockaddr *)&addr, sizeof(addr)))
		return (philovisualizer_final());
	atexit(philovisualizer_final);
}

static void	philovisualizer_final(void)
{
	if (sock < 0)
		return ;
	close(sock);
	sock = -1;
}

void	philovisualizer_send(unsigned int philo, pv_code code)
{
	pv_data	data;

	if (sock < 0)
		return ;
	data.var.philo = philo;
	data.var.code = code;
	send(sock, data.data, sizeof(data), 0);
}
