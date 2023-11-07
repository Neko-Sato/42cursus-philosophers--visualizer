#include "philo_visualizer.h"
#include <fcntl.h>
#include <sys/stat.h>
#include <unistd.h>

static int	fd = -1;


void	philovisualizer_init(unsigned int len, int isbouns)
{
	// unlink(PV_PATH);
	// mkfifo(PV_PATH, S_IWUSR | S_IRUSR);
	fd = open(PV_PATH, O_WRONLY);
	if (isbouns)
		philovisualizer_send(len, PVB_INIT);
	else
		philovisualizer_send(len, PV_INIT);
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
