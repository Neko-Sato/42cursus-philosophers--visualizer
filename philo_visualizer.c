#include "philo_visualizer.h"
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

static int sock = -1;

void philovisualizer_init(void)
{
	struct sockaddr_in addr;

	sock = socket(AF_INET, SOCK_STREAM, 0);
	if (sock < 0)
		return;
	addr.sin_family = AF_INET;
	addr.sin_port = htons(PORT);
	addr.sin_addr.s_addr = inet_addr(ADDRESS);
	if (connect(sock, (struct sockaddr *)&addr, sizeof(addr)))
		return philovisualizer_final();
}

void philovisualizer_final(void)
{
	close(sock);
	sock = -1;
}

void	philovisualizer_send(unsigned int philo, pv_code code)
{
	pv_data data;

	if (sock < 0)
		return;
	data.var.philo = philo;
	data.var.code = code;
	send(sock, data.data, sizeof(data), 0);
}
