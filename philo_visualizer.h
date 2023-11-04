#ifndef PHILO_VISUAL_H
# define PHILO_VISUAL_H

#define PV_PATH "/tmp/philo_visualizer.sock"

typedef union
{
	char 				data[8];
	struct
	{
		unsigned int	philo;
		unsigned int	code;
	} var;

}	pv_data;

typedef enum
{
	PV_THINKING		= 0b0000u,
	PV_EATING		= 0b0001u,
	PV_SLEEPING		= 0b0010u,
	PV_DIED			= 0b0011u,
	PV_TAKE_LEFT	= 0b0100u,
	PV_PUT_LEFT		= 0b0101u,
	PV_TAKE_RIGHT	= 0b0110u,
	PV_PUT_RIGHT	= 0b0111u,
	PVB_TAKE		= 0b0100u,
	PVB_PUT			= 0b0101u,
	PV_RESET		= 0b1000u,
}	pv_code;

void	philovisualizer_init(void);

void	philovisualizer_send(unsigned int philo, pv_code code);

#endif