#include "philo_visualizer.h"
#include <unistd.h>

void	philovisualizer_send(unsigned int philo, pv_code code)
{
	pv_data data;

	data.var.philo = philo;
	data.var.code = code;
	write(1, data.data, sizeof(data));
}
