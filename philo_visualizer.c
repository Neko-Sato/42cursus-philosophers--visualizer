#include "philo_visualizer.h"
#include <fcntl.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <unistd.h>

static int	fd = -1;

static void	philovisualizer_final(void);

void	philovisualizer_init(unsigned int len, int isbouns)
{
	if (access(PV_PATH, F_OK))
		mkfifo(PV_PATH, S_IWUSR | S_IRUSR);
	fd = open(PV_PATH, O_WRONLY);
	atexit(philovisualizer_final);
	if (isbouns)
		philovisualizer_send(len, PVB_INIT);
	else
		philovisualizer_send(len, PV_INIT);
}

static void	philovisualizer_final(void)
{
	if (fd < 0)
		return ;
	close(fd);
	fd = -1;
}

void	philovisualizer_send(unsigned int philo, pv_code code)
{
	pv_data	data;

	if (fd < 0)
		return ;
	data.var.philo = philo;
	data.var.code = code;
	write(fd, data.data, sizeof(data));
}
