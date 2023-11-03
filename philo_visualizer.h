#ifndef PHILO_VISUAL
# define PHILO_VISUAL

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
	PV_THINKING		= 0b000u,
	PV_EATING		= 0b001u,
	PV_SLEEPING		= 0b010u,
	PV_DIED			= 0b011u,
	PV_TAKE_LEFT	= 0b100u,
	PV_PUT_LEFT		= 0b100u,
	PV_TAKE_RIGHT	= 0b100u,
	PV_PUT_RIGHT	= 0b100u,
}	pv_code;

void	philovisualizer_send(unsigned int philo, pv_code code);

#endif